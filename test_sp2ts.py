#!/usr/bin/python3
"""
Unit tests for the sp2ts library.

.. code:: console

    $ python Tests\test_sp2ts.py

Jamie Taylor 2020-03-31
"""

import unittest
from datetime import datetime
import pytz

from sp2ts import to_unixtime, from_unixtime, sp2ts, ts2sp

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

        Test settlement periods:
            2020-03-28 SP24 (GMT) <-> SP ending 2020-03-28T12:00:00Z <-> SP ending 1585396800
            2020-03-29 SP24 (BST) <-> SP ending 2020-03-29T12:00:00Z <-> SP ending 1585483200
            2020-03-30 SP24 (BST) <-> SP ending 2020-03-30T11:00:00Z <-> SP ending 1585566000
            2019-10-26 SP24 (BST) <-> SP ending 2019-10-26T11:00:00Z <-> SP ending 1572087600
            2019-10-27 SP24 (GMT) <-> SP ending 2019-10-27T11:00:00Z <-> SP ending 1572174000
            2019-10-28 SP24 (GMT) <-> SP ending 2019-10-28T12:00:00Z <-> SP ending 1572264000
        """
        d1 = datetime(2020, 3, 28).date()
        d2 = datetime(2020, 3, 29).date()
        d3 = datetime(2020, 3, 30).date()
        d4 = datetime(2019, 10, 26).date()
        d5 = datetime(2019, 10, 27).date()
        d6 = datetime(2019, 10, 28).date()
        sp = 24
        self.assertEqual(sp2ts(d1, sp), 1585396800)
        self.assertEqual(sp2ts(d2, sp), 1585483200)
        self.assertEqual(sp2ts(d3, sp), 1585566000)
        self.assertEqual(sp2ts(d4, sp), 1572087600)
        self.assertEqual(sp2ts(d5, sp), 1572174000)
        self.assertEqual(sp2ts(d6, sp), 1572264000)

    def test_ts2sp(self):
        """
        Test the `ts2sp()` function.

        See circulars from Elexon in the Docs directory for settlement period convention on days
        where GB transitions from GMT to BST and vice versa.

        Test settlement periods:
            2020-03-28 SP24 (GMT) <-> SP ending 2020-03-28T12:00:00Z <-> SP ending 1585396800
            2020-03-29 SP24 (BST) <-> SP ending 2020-03-29T12:00:00Z <-> SP ending 1585483200
            2020-03-30 SP24 (BST) <-> SP ending 2020-03-30T11:00:00Z <-> SP ending 1585566000
            2019-10-26 SP24 (BST) <-> SP ending 2019-10-26T11:00:00Z <-> SP ending 1572087600
            2019-10-27 SP24 (GMT) <-> SP ending 2019-10-27T11:00:00Z <-> SP ending 1572174000
            2019-10-28 SP24 (GMT) <-> SP ending 2019-10-28T12:00:00Z <-> SP ending 1572264000
        """
        d1 = datetime(2020, 3, 28).date()
        d2 = datetime(2020, 3, 29).date()
        d3 = datetime(2020, 3, 30).date()
        d4 = datetime(2019, 10, 26).date()
        d5 = datetime(2019, 10, 27).date()
        d6 = datetime(2019, 10, 28).date()
        sp = 24
        self.assertEqual(ts2sp(1585396800), (d1, sp))
        self.assertEqual(ts2sp(1585483200), (d2, sp))
        self.assertEqual(ts2sp(1585566000), (d3, sp))
        self.assertEqual(ts2sp(1572087600), (d4, sp))
        self.assertEqual(ts2sp(1572174000), (d5, sp))
        self.assertEqual(ts2sp(1572264000), (d6, sp))

if __name__ == "__main__":
    unittest.main()
