from gtfspy.import_loaders.table_loader import TableLoader


class DayTripsMaterializer(TableLoader):
    """Make the table day_trips with (date, trip_I, start, end, day_start_ut).

    This replaces the old day_trips view.  This allows direct querying
    on the start_time_ut and end_time_ut, at the cost that this table is
    now O(days * trips).  This makes the following things:

    day_trips2: The actual table
    day_trips: Replacement for the old day_trips view.  day_trips2+trips
    day_stop_times: day_trips2+trips+stop_times
    """
    fname = None
    table = 'day_trips2'
    tabledef = ('(date TEXT, '
                'trip_I INT, '
                'start_time_ut INT, '
                'end_time_ut INT, '
                'day_start_ut INT)')
    copy_where = 'WHERE  {start_ut} < end_time_ut  AND  start_time_ut < {end_ut}'

    @classmethod
    def post_import_round2(cls, conn):
        cur = conn.cursor()
        cur.execute('INSERT INTO day_trips2 '
                    'SELECT date, trip_I, '
                    'days.day_start_ut+trips.start_time_ds AS start_time_ut, '
                    'days.day_start_ut+trips.end_time_ds AS end_time_ut, '
                    'day_start_ut '
                    'FROM days '
                    'JOIN trips USING (trip_I)')
        conn.commit()

    def index(cls, cur):
        cur.execute('CREATE INDEX IF NOT EXISTS idx_day_trips2_tid '
                    'ON day_trips2 (trip_I)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_day_trips2_d '
                    'ON day_trips2 (date)')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_day_trips2_stut_etut '
                    'ON day_trips2 (start_time_ut, end_time_ut)')
        # This index may not be needed anymore.
        cur.execute('CREATE INDEX IF NOT EXISTS idx_day_trips2_dsut '
                    'ON day_trips2 (day_start_ut)')

    @classmethod
    def make_views(cls, conn):
        """Create day_trips and day_stop_times views.

        day_trips:  day_trips2 x trips  = days x trips
        day_stop_times: day_trips2 x trips x stop_times = days x trips x stop_times
        """
        conn.execute('DROP VIEW IF EXISTS main.day_trips')
        conn.execute('CREATE VIEW day_trips AS   '
                     'SELECT day_trips2.*, trips.* '
                     #'days.day_start_ut+trips.start_time_ds AS start_time_ut, '
                     #'days.day_start_ut+trips.end_time_ds AS end_time_ut   '
                     'FROM day_trips2 JOIN trips USING (trip_I);')
        conn.commit()

        conn.execute('DROP VIEW IF EXISTS main.day_stop_times')
        conn.execute('CREATE VIEW day_stop_times AS   '
                     'SELECT day_trips2.*, trips.*, stop_times.*, '
                     #'days.day_start_ut+trips.start_time_ds AS start_time_ut, '
                     #'days.day_start_ut+trips.end_time_ds AS end_time_ut, '
                     'day_trips2.day_start_ut+stop_times.arr_time_ds AS arr_time_ut, '
                     'day_trips2.day_start_ut+stop_times.dep_time_ds AS dep_time_ut   '
                     'FROM day_trips2 '
                     'JOIN trips USING (trip_I) '
                     'JOIN stop_times USING (trip_I)')
        conn.commit()