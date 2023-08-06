# -*- coding: utf-8 -*-
import re
import datetime

class Quartermaster(object):
    """
    Calculate fiscal quarter and day for gregorian calendar.
    If you want fiscal weeks, I feel your pain.

    Usage:
    # assuming today's date is 2017-9-2
    >>> from quartermaster import Quartermaster
    >>> qm = Quartermaster()
    >>> qm.quarter
    3
    >>> qm.day
    245
    >>>

    # a "now" in the past or future may be provided in iso date format ...
    >>> qm = Quartermaster(now="1966-06-18")
    >>> qm.quarter
    2
    >>> qm.day
    169
    >>> 

    # ... or as a datetime object
    >>> now = datetime.date(1968, 10, 18)
    >>> qm = Quartermaster(now=now)
    >>> qm.quarter
    3
    >>> qm.day
    245
    >>> 

    # With a fiscal year that runs October 1 - September 1
    >>> now = datetime.date(2017, 1, 1)
    >>> qm = Quartermaster(fismonth=10, fisday=1, now=now)
    >>> qm.quarter
    2
    >>> qm.day
    93
    >>>
    """

    def __init__(self, fismonth=1, fisday=1, now=False):
        """
        Default fiscal year starts w/calendar year. 
        """
        if now:
            if isinstance(now, str):
                assert re.match("\d\d\d\d-\d\d-\d\d", now)
                year, month, day = now.split("-")
                now = datetime.date(int(year), int(month), int(day))
            else:
                assert isinstance(now, datetime.date)
        else:
            now = datetime.date.today()

        fisstart = datetime.date(now.year, fismonth, fisday)

        self.quarter = self.get_quarter(now, fisstart)
        self.day = self.get_day(now, fisstart)

        self.now = now
        self.fisstart = fisstart

    def get_day(self, now, fisstart):
        """
        Get now's fiscal day
        """
        for i in range(1, 367):
            if (fisstart.month, fisstart.day) == (now.month, now.day):
                return i
            fisstart += datetime.timedelta(days=1)

    def get_quarter(self, now, fisstart):
        """
        Get now's fiscal quarter
        """
        month = fisstart.month
        ml = [fisstart.month]
        for i in range(12):
            month += 1
            if month == 13:
                month = 1
            ml.append(month)
        quarters = [ml[:3], ml[3:6], ml[6:9], ml[9:12],]
        for q, m, in enumerate(quarters):
            if now.month in m:
                return q+1
