try:
    #py2
    from sp2ts import sp2ts, to_unixtime, from_unixtime, sp2ts, ts2sp, dt2sp
except:
    #py3+
    from sp2ts import sp2ts, to_unixtime, from_unixtime, sp2ts, ts2sp, dt2sp

__all__ = ["sp2ts", "to_unixtime", "from_unixtime", "sp2ts", "ts2sp", "dt2sp"]