#!/usr/bin/env python3
"""
Example usage of the sp2ts module.

- Jamie Taylor <jamie.taylor@sheffield.ac.uk>
- First Authored: 2020-03-31

"""

from datetime import date

from sp2ts import sp2ts, ts2sp, from_unixtime


def main():
    # Converting date and SP to timestamp...
    mydate = date(2020, 3, 28)
    mysp = 24
    mytimestamp = sp2ts(mydate, mysp)
    print(f"{mydate} SP{mysp}  -->  {mytimestamp} ({from_unixtime(mytimestamp)})")
    # Converting timestamp to date and SP...
    mytimestamp = 1585396800  # SP ending 2020-03-28T12:00:00Z
    mydate, mysp = ts2sp(mytimestamp)
    print(f"{mytimestamp} ({from_unixtime(mytimestamp)})  -->  {mydate} SP{mysp}")


if __name__ == "__main__":
    main()
