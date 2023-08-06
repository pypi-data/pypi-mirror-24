#!/usr/bin/env python
import datetime
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from quartermaster import Quartermaster


"""
quarters for standard US fiscal calendar 2017
Q1 2017 -- January 1, 2017 to March 31, 2017
Q2 2017 -- April 1, 2017 to June 30, 2017
Q3 2017 -- July 1, 2017 to September 30, 2017
Q4 2017 -- October 1, 2017 to December 31, 2017
"""

qm = Quartermaster(now=datetime.date(2017, 1, 1))
assert qm.quarter == 1 
qm = Quartermaster(now=datetime.date(2017, 3, 31))
assert qm.quarter == 1 

qm = Quartermaster(now=datetime.date(2017, 4, 1))
assert qm.quarter == 2
qm = Quartermaster(now=datetime.date(2017, 6, 30))
assert qm.quarter == 2

qm = Quartermaster(now=datetime.date(2017, 7, 1))
assert qm.quarter == 3
qm = Quartermaster(now=datetime.date(2017, 9, 30))
assert qm.quarter == 3

qm = Quartermaster(now=datetime.date(2017, 10, 1))
assert qm.quarter == 4
qm = Quartermaster(now=datetime.date(2017, 12, 31))
assert qm.quarter == 4

"""
quarters for standard US gov fiscal calendar 2017
Q1 2017 -- October 1, 2016 to December 31, 2016
Q2 2017 -- January 1, 2017 to March 31, 2017
Q3 2017 -- April 1, 2017 to June 30, 2017
Q4 2017 -- July 1, 2017 to September 30, 2017
"""
qm = Quartermaster(fismonth=10, fisday=1, now=datetime.date(2016, 10, 1))
assert qm.quarter == 1 
qm = Quartermaster(fismonth=10, fisday=1, now=datetime.date(2016, 12, 31))
assert qm.quarter == 1 

qm = Quartermaster(fismonth=10, fisday=1, now=datetime.date(2017, 1, 1))
assert qm.quarter == 2 
qm = Quartermaster(fismonth=10, fisday=1, now=datetime.date(2017, 3, 31))
assert qm.quarter == 2 

qm = Quartermaster(fismonth=10, fisday=1, now=datetime.date(2017, 4, 1))
assert qm.quarter == 3 
qm = Quartermaster(fismonth=10, fisday=1, now=datetime.date(2017, 6, 30))
assert qm.quarter == 3 

qm = Quartermaster(fismonth=10, fisday=1, now=datetime.date(2017, 7, 1))
assert qm.quarter == 4 
qm = Quartermaster(fismonth=10, fisday=1, now=datetime.date(2017, 9, 30))
assert qm.quarter == 4 

now = datetime.date.today()
qm = Quartermaster()
usg = Quartermaster(fismonth=10, fisday=1)
print("Today is: %s, q%s, (q%s USG)"%(now, qm.quarter, usg.quarter))
