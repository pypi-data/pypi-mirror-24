from collections import defaultdict, Counter
import sys

# the following is required when using this module as a script
# (i.e. using the if __name__ == "__main__": part at the end of this file)
if __name__ == '__main__' and __package__ is None:
    # import gtfspy
    __package__ = 'gtfspy'


from gtfspy import route_types
from gtfspy.gtfs import GTFS
from gtfspy.util import wgs84_distance

WARNING_LONG_STOP_SPACING = "Long Stop Spacing"
WARNING_5_OR_MORE_CONSECUTIVE_STOPS_WITH_SAME_TIME = "Trips that have Five or More Consecutive Same Stop Times"
WARNING_LONG_TRIP_TIME = "Long Trip Time"
WARNING_UNREALISTIC_AVERAGE_SPEED = "Unrealistic Average Speed"
WARNING_LONG_TRAVEL_TIME_BETWEEN_STOPS = "Long Travel Time Between Consecutive Stops"
WARNING_STOP_SEQUENCE_ERROR = "Stop Sequence Error"
WARNING_STOP_FAR_AWAY_FROM_FILTER_BOUNDARY = "Stop far away from spatial filter boundary"

ALL_WARNINGS = {
    WARNING_LONG_STOP_SPACING,
    WARNING_5_OR_MORE_CONSECUTIVE_STOPS_WITH_SAME_TIME,
    WARNING_LONG_TRIP_TIME,
    WARNING_UNREALISTIC_AVERAGE_SPEED,
    WARNING_LONG_TRAVEL_TIME_BETWEEN_STOPS,
    WARNING_STOP_SEQUENCE_ERROR
}


class TimetableValidator(object):

    def __init__(self, gtfs, buffer_params=None):
        """
        Parameters
        ----------
        gtfs: GTFS, or path to a GTFS object
            A GTFS object
        """
        if not isinstance(gtfs, GTFS):
            self.gtfs = GTFS(gtfs)
        else:
            self.gtfs = gtfs
        self.buffer_params = buffer_params
        self.warnings_container = WarningsContainer()

    def get_warnings(self):
        """
        Validates/checks a given GTFS feed with respect to a number of different issues.

        The set of warnings that are checked for, can be found in the gtfs_validator.ALL_WARNINGS

        Returns
        -------
        warnings: WarningsContainer
        """
        self.warnings_container.clear()
        self._validate_stops_with_same_stop_time()
        self._validate_speeds_and_trip_times()
        self._validate_stop_spacings()
        self._validate_stop_sequence()
        self._validate_misplaced_stops()
        self.warnings_container.print_summary()
        return self.warnings_container

    def _validate_misplaced_stops(self):
        if self.buffer_params:
            p = self.buffer_params
            center_lat = p['lat']
            center_lon = p['lon']
            distance = p['buffer_distance'] * 2 * 1000
            count = 0
            for stop_row in self.gtfs.stops().itertuples():
                if distance < wgs84_distance(center_lat, center_lon, stop_row.lat, stop_row.lon):
                    self.warnings_container.add_warning(stop_row, WARNING_STOP_FAR_AWAY_FROM_FILTER_BOUNDARY)
                    print(WARNING_STOP_FAR_AWAY_FROM_FILTER_BOUNDARY, stop_row)

    def _validate_stops_with_same_stop_time(self):
        n_stops_with_same_time = 5
        # this query returns the trips where there are N or more stops with the same stop time
        rows = self.gtfs.get_cursor().execute(
            'SELECT '
            'trip_I, '
            'arr_time, '
            'N '
            'FROM '
            '(SELECT trip_I, arr_time, count(*) as N FROM stop_times GROUP BY trip_I, arr_time) q1 '
            'WHERE N >= ?', (n_stops_with_same_time,)
        )
        for row in rows:
            self.warnings_container.add_warning(row, WARNING_5_OR_MORE_CONSECUTIVE_STOPS_WITH_SAME_TIME)

    def _validate_stop_spacings(self):
        self.gtfs.conn.create_function("find_distance", 4, wgs84_distance)
        max_stop_spacing = 20000  # meters
        max_time_between_stops = 1800  # seconds
        # this query calculates distance and travel time between consecutive stops
        rows = self.gtfs.execute_custom_query(
            'SELECT '
            'q1.trip_I, '
            'type, '
            'q1.stop_I as stop_1, '
            'q2.stop_I as stop_2, '
            'CAST(find_distance(q1.lat, q1.lon, q2.lat, q2.lon) AS INT) as distance, '
            'q2.arr_time_ds - q1.arr_time_ds as traveltime '
            'FROM '
            '(SELECT * FROM stop_times, stops WHERE stop_times.stop_I = stops.stop_I) q1, '
            '(SELECT * FROM stop_times, stops WHERE stop_times.stop_I = stops.stop_I) q2, '
            'trips, '
            'routes '
            'WHERE q1.trip_I = q2.trip_I '
            'AND q1.seq + 1 = q2.seq '
            'AND q1.trip_I = trips.trip_I '
            'AND trips.route_I = routes.route_I ').fetchall()
        for row in rows:
            if row[4] > max_stop_spacing:
                self.warnings_container.add_warning(row, WARNING_LONG_STOP_SPACING)
            if row[5] > max_time_between_stops:
                self.warnings_container.add_warning(row, WARNING_LONG_TRAVEL_TIME_BETWEEN_STOPS)

    def _validate_speeds_and_trip_times(self):
        # These are the mode - feasible speed combinations used here:
        # https://support.google.com/transitpartners/answer/1095482?hl=en
        gtfs_type_to_max_speed = {
            route_types.TRAM     : 100,
            route_types.SUBWAY   : 150,
            route_types.RAIL     : 300,
            route_types.BUS      : 100,
            route_types.FERRY    : 80,
            route_types.CABLE_CAR: 50,
            route_types.GONDOLA  : 50,
            route_types.FUNICULAR: 50,
            route_types.AIRCRAFT : 1000
        }
        max_trip_time = 7200  # seconds
        self.gtfs.conn.create_function("find_distance", 4, wgs84_distance)

        # this query returns the total distance and travel time for each trip calculated for each stop spacing separately
        rows = self.gtfs.execute_custom_query(
            'SELECT '
            ' q1.trip_I, '
            ' type, '
            ' sum(CAST(find_distance(q1.lat, q1.lon, q2.lat, q2.lon) AS INT)) AS total_distance, '
            ' sum(q2.arr_time_ds - q1.arr_time_ds) AS total_traveltime '
            ' FROM '
            '(SELECT * FROM stop_times, '
            'stops WHERE stop_times.stop_I = stops.stop_I) q1, '
            '(SELECT * FROM stop_times, '
            'stops WHERE stop_times.stop_I = stops.stop_I) q2, trips, routes WHERE q1.trip_I = q2.trip_I '
            'AND q1.seq + 1 = q2.seq AND q1.trip_I = trips.trip_I '
            '  AND trips.route_I = routes.route_I GROUP BY q1.trip_I').fetchall()

        for row in rows:
            avg_velocity = row[2] / max(row[3], 1) * 3.6
            if avg_velocity > gtfs_type_to_max_speed[row[1]]:
                self.warnings_container.add_warning(row, WARNING_UNREALISTIC_AVERAGE_SPEED)

            if row[3] > max_trip_time:
                self.warnings_container.add_warning(row, WARNING_LONG_TRIP_TIME)

    def _validate_stop_sequence(self):
        # this function checks if the stop sequence value is changing with +1 for each stop. This is not (yet) enforced
        rows = self.gtfs.execute_custom_query('SELECT trip_I, dep_time_ds, seq '
                                              'FROM stop_times '
                                              'ORDER BY trip_I, dep_time_ds, seq').fetchall()

        old_trip_id = None
        for row in rows:
            new_trip_id = row[0]
            new_seq = row[2]
            if old_trip_id == new_trip_id:
                if old_seq + 1 != new_seq:
                    self.warnings_container.add_warning(row, WARNING_STOP_SEQUENCE_ERROR)
            old_trip_id = row[0]
            old_seq = row[2]


class WarningsContainer(object):

    def __init__(self):
        self._warnings_counter = Counter()
        # key: "warning type" string, value: "number of errors" int
        self._warnings_records = defaultdict(list)
        # key: "row that produced error" tuple, value: list of "warning type(s)" string

    def add_warning(self, row, error, value=None):
        if value:
            self._warnings_counter[error] += value
        else:
            self._warnings_counter[error] += 1
        self._warnings_records[row].append(error)

    def print_summary(self):
        print('The feed produced the following warnings: ')
        for key in self._warnings_counter.keys():
            print(key + ": " + str(self._warnings_counter[key]))

    def get_warning_counts(self):
        """
        Returns
        -------
        counter: collections.Counter
        """
        return self._warnings_counter

    def get_warnings_by_query_rows(self):
        """
        Returns
        -------
        warnings_record: defaultdict(list)
            maps each row to a list of warnings
        """
        return self._warnings_records

    def clear(self):
        self._warnings_counter.clear()
        self._warnings_records.clear()


def main():
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "validate":
        validator = TimetableValidator(args[0])
        warningscontainer = validator.get_warnings()
        warningscontainer.print_summary()

if __name__ == "__main__":
    main()

