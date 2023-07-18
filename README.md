# sp2ts
A Python module for converting between the settlement periods used by GB electricity industry and Unix timestamps.

## What is this repository for? ##

* Convert date and settlement period to Unix timestamp and vice versa.
* Convert date and settlement period to Python datetime object and vice versa.
* Convert Python datetime objects to Unix timestamp and vice versa.
* Version 0.2.1
* Developed and tested with Python 3.9, should work for 3.6+.

## How do I get set up? ##

Make sure you have Git installed - [Download Git](https://git-scm.com/downloads)

Run `pip install sp2ts`

(or `pip install git+https://github.com/SheffieldSolar/sp2ts/`)

Check that the installation was successful by running the following command from terminal / command-line:

```>> sp2ts -h```

This will print the helper for the command line interface which can be useful for working interactively:

```
usage: sp2ts.py [-h] [-d <yyyy-mm-dd>] [-sp <[1..50]>]
                [-ts <seconds since epoch>] [-dt <yyyy-mm-ddTHH:MM:SS>]
                [-tz <Olson timezone string>]

This is a command line interface (CLI) for the sp2ts module.

optional arguments:
  -h, --help            show this help message and exit
  -d <yyyy-mm-dd>, --date <yyyy-mm-dd>
                        Specify a date (use only in conjuction with
                        -sp/--settlement-period).
  -sp <[1..50]>, --settlement-period <[1..50]>
                        Specify a settlement period (use only in conjuction
                        with -d/--date).
  -ts <seconds since epoch>, --timestamp <seconds since epoch>
                        Specify a timestamp (all other options will be
                        ignored).
  -dt <yyyy-mm-ddTHH:MM:SS>, --datetime <yyyy-mm-ddTHH:MM:SS>
                        Specify a datetime (optionally also specify
                        -tz/--timezone).
  -tz <Olson timezone string>, --timezone <Olson timezone string>
                        Specify a timezone (used only in conjunction with
                        -dt/--datetime, default is 'UTC').

Jamie Taylor, 2020-03-31
```

## Usage ##

The module contains the following functions:

* `to_unixtime(datetime, timezone=None)`
    - Convert a Python datetime object to Unix timestamp. The datetime object must be timezone aware or else you must pass the timezone as an Olsen timezone string.
* `from_unixtime(timestamp, timezone="UTC")`
    - Convert a Unix timestamp to a (timezone-aware) Python datetime object
* `sp2ts(date, sp, closed="right")`
    - Convert a date and settlement period into a Unix timestamp. The `closed` parameter can be `"left"`, `"middle"` or `"right"` (default), which will determine whether the timestamp returned is the start, middle or end of the settlement period respectively.
* `sp2dt(date, sp, closed="right")`
    - Convert a date and settlement period into a (timezone-aware) Python datetime object. The `closed` parameter can be `"left"`, `"middle"` or `"right"` (default), which will determine whether the timestamp returned is the start, middle or end of the settlement period respectively.
* `ts2sp(timestamp)`
    - Convert a Unix timestamp into a date and settlement period. Settlement periods are considered to be "closed right" i.e. SP 1 refers to the interval 00:00:00 < t <= 00:30:00.
* `dt2sp(datetime, timezone=None)`
    - Convert a Python datetime object into a date and settlement period. The `datetime` must be timezone-aware, or else you must also pass the `timezone` as an Olsen timezone string. Settlement periods are considered to be "closed right" i.e. SP 1 refers to the interval 00:00:00 < t <= 00:30:00.

### Example ###
```
from datetime import date

from sp2ts import sp2ts, ts2sp, from_unixtime

def main():
    # Converting date and SP to timestamp...
    mydate = date(2020, 3, 28)
    mysp = 24
    mytimestamp = sp2ts(mydate, mysp)
    print(f"{mydate} SP{mysp}  -->  {mytimestamp} ({from_unixtime(mytimestamp)})")
    # Converting timestamp to date and SP...
    mytimestamp = 1585396800 # SP ending 2020-03-28T12:00:00Z
    mydate, mysp = ts2sp(mytimestamp)
    print(f"{mytimestamp} ({from_unixtime(mytimestamp)})  -->  {mydate} SP{mysp}")

if __name__ == "__main__":
    main()
```

> 2020-03-28 SP24  -->  1585396800 (2020-03-28 12:00:00+00:00)

> 1585396800 (2020-03-28 12:00:00+00:00)  -->  2020-03-28 SP24

## How do I update? ##

Run `pip3 install --upgrade git+https://github.com/SheffieldSolar/sp2ts/`.

## How do I run tests? ##

Clone the repo locally, then run the following command from the repo's root:

```>> python -m Tests.test_sp2ts```
