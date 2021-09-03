#!/usr/bin/python3
"""
Unit tests for the sp2ts library.

.. code:: console

    $ python Tests\test_sp2ts.py

Jamie Taylor 2020-03-31
"""

import unittest
from datetime import datetime, date
import pytz

from sp2ts import to_unixtime, from_unixtime, sp2ts, ts2sp

TEST_VALUES = [ # Should probably load these from file or at least a separate module for neatness
    # --- Test SP 24 around clock change ---
    # 2020-03-28 SP24 (GMT) <-> SP ending 2020-03-28T12:00:00Z <-> SP ending 1585396800
    {
        "sp": (date(2020, 3, 28), 24),
        "dt": datetime(2020, 3, 28, 12, tzinfo=pytz.utc),
        "ts": 1585396800
    },
    # 2020-03-29 SP24 (GMT...BST) <-> SP ending 2020-03-29T12:00:00Z <-> SP ending 1585483200
    {
        "sp": (date(2020, 3, 29), 24),
        "dt": datetime(2020, 3, 29, 12, tzinfo=pytz.utc),
        "ts": 1585483200
    },
    # 2020-03-30 SP24 (BST) <-> SP ending 2020-03-30T11:00:00Z <-> SP ending 1585566000
    {
        "sp": (date(2020, 3, 30), 24),
        "dt": datetime(2020, 3, 30, 11, tzinfo=pytz.utc),
        "ts": 1585566000
    },
    # 2019-10-26 SP24 (BST) <-> SP ending 2019-10-26T11:00:00Z <-> SP ending 1572087600
    {
        "sp": (date(2019, 10, 26), 24),
        "dt": datetime(2019, 10, 26, 11, tzinfo=pytz.utc),
        "ts": 1572087600
    },
    # 2019-10-27 SP24 (BST...GMT) <-> SP ending 2019-10-27T11:00:00Z <-> SP ending 1572174000
    {
        "sp": (date(2019, 10, 27), 24),
        "dt": datetime(2019, 10, 27, 11, tzinfo=pytz.utc),
        "ts": 1572174000
    },
    # 2019-10-28 SP24 (GMT) <-> SP ending 2019-10-28T12:00:00Z <-> SP ending 1572264000
    {
        "sp": (date(2019, 10, 28), 24),
        "dt": datetime(2019, 10, 28, 12, tzinfo=pytz.utc),
        "ts": 1572264000
    },
    # --- Test SP at start end end of day around clock change ---
    # 2021-03-27 SP1 (GMT) (48 SPs) <-> SP ending 2021-03-27T00:30:00Z <-> SP ending 1616805000
    {
        "sp": (date(2021, 3, 27), 1),
        "dt": datetime(2021, 3, 27, 0, 30, tzinfo=pytz.utc),
        "ts": 1616805000
    },
    # 2021-03-27 SP48 (GMT) (48 SPs) <-> SP ending 2021-03-28T00:00:00Z <-> SP ending 1616889600
    {
        "sp": (date(2021, 3, 27), 48),
        "dt": datetime(2021, 3, 28, 0, 0, tzinfo=pytz.utc),
        "ts": 1616889600
    },
    # 2021-03-28 SP1 (GMT...BST) (46 SPs) <-> SP ending 2021-03-28T00:30:00Z <-> SP ending 1616891400
    {
        "sp": (date(2021, 3, 28), 1),
        "dt": datetime(2021, 3, 28, 0, 30, tzinfo=pytz.utc),
        "ts": 1616891400
    },
    # 2021-03-28 SP46 (GMT...BST) (46 SPs) <-> SP ending 2021-03-28T23:00:00Z <-> SP ending 1616972400
    {
        "sp": (date(2021, 3, 28), 46),
        "dt": datetime(2021, 3, 28, 23, 30, tzinfo=pytz.utc),
        "ts": 1616972400
    },
    # 2021-03-29 SP1 (BST) (48 SPs) <-> SP ending 2021-03-28T23:30:00Z <-> SP ending 1616974200
    {
        "sp": (date(2021, 3, 29), 1),
        "dt": datetime(2021, 3, 28, 23, 30, tzinfo=pytz.utc),
        "ts": 1616974200
    },
    # 2021-03-29 SP2 (BST) (48 SPs) <-> SP ending 2021-03-29T00:00:00Z <-> SP ending 1616976000
    {
        "sp": (date(2021, 3, 29), 2),
        "dt": datetime(2021, 3, 29, 0, 0, tzinfo=pytz.utc),
        "ts": 1616976000
    },
    # 2021-03-29 SP3 (BST) (48 SPs) <-> SP ending 2021-03-29T00:30:00Z <-> SP ending 1616977800
    {
        "sp": (date(2021, 3, 29), 3),
        "dt": datetime(2021, 3, 29, 0, 30, tzinfo=pytz.utc),
        "ts": 1616977800
    },
    # 2021-10-30 SP1 (BST) (48 SPs) <-> SP ending 2021-10-29T23:30:00Z <-> SP ending 1635550200
    {
        "sp": (date(2021, 10, 30), 1),
        "dt": datetime(2021, 10, 29, 23, 30, tzinfo=pytz.utc),
        "ts": 1635550200
    },
    # 2021-10-30 SP48 (BST) (48 SPs) <-> SP ending 2021-10-30T23:00:00Z <-> SP ending 1635634800
    {
        "sp": (date(2021, 10, 30), 48),
        "dt": datetime(2021, 10, 30, 23, 0, tzinfo=pytz.utc),
        "ts": 1635634800
    },
    # 2021-10-31 SP1 (BST..GMT) (50 SPs) <-> SP ending 2021-10-30T23:30:00Z <-> SP ending 1635636600
    {
        "sp": (date(2021, 10, 31), 1),
        "dt": datetime(2021, 10, 30, 23, 30, tzinfo=pytz.utc),
        "ts": 1635636600
    },
    # 2021-10-31 SP48 (BST..GMT) (50 SPs) <-> SP ending 2021-10-31T23:00:00Z <-> SP ending 1635721200
    {
        "sp": (date(2021, 10, 31), 48),
        "dt": datetime(2021, 10, 31, 23, 0, tzinfo=pytz.utc),
        "ts": 1635721200
    },
    # 2021-10-31 SP50 (BST..GMT) (50 SPs) <-> SP ending 2021-11-01T00:00:00Z <-> SP ending 1635724800
    {
        "sp": (date(2021, 10, 31), 50),
        "dt": datetime(2021, 11, 1, 0, 0, tzinfo=pytz.utc),
        "ts": 1635724800
    },
    # 2021-11-01 SP1 (GMT) (48 SPs) <-> SP ending 2021-11-01T00:30:00Z <-> SP ending 1635726600
    {
        "sp": (date(2021, 11, 1), 1),
        "dt": datetime(2021, 11, 1, 0, 30, tzinfo=pytz.utc),
        "ts": 1635726600
    },
    # 2021-11-01 SP48 (GMT) (48 SPs) <-> SP ending 2021-11-02T00:00:00Z <-> SP ending 1635811200
    {
        "sp": (date(2021, 11, 1), 48),
        "dt": datetime(2021, 11, 2, 0, 0, tzinfo=pytz.utc),
        "ts": 1635811200
    },
]

class sp2tsTestCase(unittest.TestCase):
    """Tests for `sp2ts.py`."""
    def test_to_unixtime(self):
        """
        Test the `to_unixtime()` function with several test cases generated using
        http://www.epochconverter.com/

        Test datetimes:
            2020-03-28 12:34:56 (GMT) -> 2020-03-28T12:34:56Z -> 1585398896
            2020-03-29 12:34:56 (BST) -> 2020-03-29T11:34:56Z -> 1585481696
        """
        dt_no_dst_naive = datetime(2020, 3, 28, 12, 34, 56, tzinfo=None)
        dt_no_dst_aware = pytz.timezone("Europe/London").localize(dt_no_dst_naive)
        dt_dst_naive = datetime(2020, 3, 29, 12, 34, 56, tzinfo=None)
        dt_dst_aware = pytz.timezone("Europe/London").localize(dt_dst_naive)
        # Test with tz_info in the datetime object  (i.e. tz-aware datetime)
        self.assertEqual(to_unixtime(dt_no_dst_aware), 1585398896)
        self.assertEqual(to_unixtime(dt_dst_aware), 1585481696)
        # Test with separate tz_info
        self.assertEqual(to_unixtime(dt_no_dst_naive, "Europe/London"), 1585398896)
        self.assertEqual(to_unixtime(dt_dst_naive, "Europe/London"), 1585481696)
        # Test validations
        self.assertRaises(Exception, to_unixtime, dt_no_dst_naive)
        self.assertRaises(Exception, to_unixtime, dt_dst_naive)

    def test_from_unixtime(self):
        """
        Test the `from_unixtime()` function with several test cases generated using
        http://www.epochconverter.com/

        Test datetimes:
            2020-03-28 12:34:56 (GMT) <-> 2020-03-28T12:34:56Z <-> 1585398896
            2020-03-29 12:34:56 (BST) <-> 2020-03-29T11:34:56Z <-> 1585481696
        """
        d1 = datetime(2020, 3, 28, 12, 34, 56, tzinfo=None)
        d2 = datetime(2020, 3, 29, 12, 34, 56, tzinfo=None)
        dt_no_dst_aware = pytz.timezone("Europe/London").localize(d1)
        dt_no_dst_aware_utc = datetime(2020, 3, 28, 12, 34, 56, tzinfo=pytz.utc)
        dt_dst_aware = pytz.timezone("Europe/London").localize(d2)
        dt_dst_aware_utc = datetime(2020, 3, 29, 11, 34, 56, tzinfo=pytz.utc)
        # Test with no tz_info in datetime object and no tz_info passed
        self.assertEqual(from_unixtime(1585398896), dt_no_dst_aware_utc)
        self.assertEqual(from_unixtime(1585481696), dt_dst_aware_utc)
        # Test with no tz_info in datetime object and tz_info passed
        self.assertEqual(from_unixtime(1585398896, "Europe/London"), dt_no_dst_aware)
        self.assertEqual(from_unixtime(1585481696, "Europe/London"), dt_dst_aware)
        self.assertEqual(from_unixtime(1585398896, "UTC"), dt_no_dst_aware_utc)
        self.assertEqual(from_unixtime(1585481696, "UTC"), dt_dst_aware_utc)

    def test_sp2ts(self):
        """
        Test the `sp2ts()` function.

        See circulars from Elexon in the Docs directory for settlement period convention on days
        where GB transitions from GMT to BST and vice versa.

        Use TEST_VALUES and also test raise error on bad date or SP (especially long-day/short-day
        during clock change).
        """
        for testval in TEST_VALUES:
            with self.subTest(test_type="values", sp=testval["sp"]):
                self.assertEqual(sp2ts(testval["sp"][0], testval["sp"][1]), testval["ts"])
        error_test_values = [
            # SP is not int -> TypeError
            {"sp": (date(2021, 3, 27), "1"), "error": TypeError},
            {"sp": (date(2021, 3, 27), "one"), "error": TypeError},
            {"sp": (date(2021, 3, 27), 1.0), "error": TypeError},
            # Date is not datetime.date -> TypeError
            {"sp": ("date(2021, 3, 27)", 1), "error": TypeError},
            {"sp": ("2021-03-21", 1), "error": TypeError},
            {"sp": (datetime(2021, 3, 27), 1), "error": TypeError},
            {"sp": (1616803200, 1), "error": TypeError},
            # SP doesn't exist -> ValueError
            {"sp": (date(2021, 3, 27), 0), "error": ValueError},
            {"sp": (date(2021, 3, 27), 49), "error": ValueError},
            {"sp": (date(2021, 3, 28), 0), "error": ValueError},
            {"sp": (date(2021, 3, 28), 47), "error": ValueError},
            {"sp": (date(2021, 3, 29), 49), "error": ValueError},
            {"sp": (date(2021, 10, 30), 49), "error": ValueError},
            {"sp": (date(2021, 10, 31), 51), "error": ValueError},
            {"sp": (date(2021, 11, 1), 49), "error": ValueError}
        ]
        for testval in error_test_values:
            with self.subTest(test_type="errors", sp=testval["sp"]):
                with self.assertRaises(testval["error"]):
                    sp2ts(date_=testval["sp"][0], sp_=testval["sp"][1])

    def test_ts2sp(self):
        """
        Test the `ts2sp()` function.

        See circulars from Elexon in the Docs directory for settlement period convention on days
        where GB transitions from GMT to BST and vice versa.

        Use TEST_VALUES and also test raise error when timestamp is wrong type or doesn't exist or 
        isn't a 30 min interval.
        """
        for testval in TEST_VALUES:
            with self.subTest(test_type="values", ts=testval["ts"]):
                self.assertEqual(ts2sp(testval["ts"]), testval["sp"])
        error_test_values = [
            # TS is not int -> TypeError
            {"ts": "1585396800", "error": TypeError},
            {"ts": 1585396800.0, "error": TypeError},
            {"ts": datetime(2020, 3, 28, 12, tzinfo=pytz.utc), "error": TypeError},
            # TS does not fall on 30 min interval -> ValueError
            {"ts": 1585396799, "error": ValueError},
            {"ts": 1585396801, "error": ValueError},
            {"ts": 1585397700, "error": ValueError},
            # TS doesn't exist or is outside supported range
            {"ts": -1, "error": ValueError},
            ## Min supported datetime is 2000-03-26T00:00:00Z i.e. 954028800
            {"ts": 954027000, "error": ValueError},
            ## Max supported datetime is 2029-10-28T00:00:00Z i.e. 1887840000
            {"ts": 1887841800, "error": ValueError},
        ]
        for testval in error_test_values:
            with self.subTest(test_type="errors", sp=testval["ts"]):
                with self.assertRaises(testval["error"]):
                    ts2sp(testval["ts"])

if __name__ == "__main__":
    unittest.main()
