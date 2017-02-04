# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 20:47:23 2017

@author: nattawutvejkanchana
"""
import datetime
def get_dates_in_month(year,month):
    
    d1 = datetime.date(2017,3,1)
    d2 = datetime.date(2017,4,1)
    
    diff = d2 - d1
    #for i in range(diff.days):
    #    print (d1 + datetime.timedelta(i))
    dates_in_month = [d1 + datetime.timedelta(i) for i in range(diff.days)]
    
    return dates_in_month
def get_week_day(date):
    return date.weekday()

def is_weekday(date):
    return get_week_day(date) < 5