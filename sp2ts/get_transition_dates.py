"""
Utility for generating a list of transition date timestamps for use in sp2ts.
Always test the outputs carefully in case there have been changes in the behvaiour of pytz or
datetime!

Jamie Taylor
2024-02-20
"""

from datetime import datetime, time
from pytz import timezone

import pandas as pd

from sp2ts import to_unixtime


def main():
    tz = timezone("Europe/London")
    transition_dates = pd.DataFrame([
        [d.year, d.date(), to_unixtime(datetime.combine(d.date(), time(0)), timezone_="UTC")]
        for d in tz._utc_transition_times[20:]
    ], columns=["year", "transition_date", "transition_date_ts"])
    transition_dates = transition_dates.loc[(transition_dates.year >= 1990)]
    transition_dates["transition_number"] = transition_dates.groupby("year")["transition_date"]\
                                                            .rank().astype("Int64")
    transition_dates_ = transition_dates.set_index(["year", "transition_number"])\
                                        .unstack(level=-1)\
                                        .reset_index()\
                                        .reset_index()\
                                        .values
    print(
        "TRANSITION_DATES_TS = [\r\n   ",
        "\r\n    ".join([f"({t[4]}, {t[5]}), # {t[1]}: {t[2]}, {t[3]}" for t in transition_dates_]),
        "\r\n]"
    )


if __name__ == "__main__":
    main()
