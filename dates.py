#!/usr/bin/env python

from datetime import date, timedelta


def get_month(today):
    month = today.strftime('%B').lower()
    return month


def get_previous_month(today):
    first_of_month = today.replace(day=1)
    prev = first_of_month - timedelta(days=1)
    prev_month = prev.strftime('%B').lower()
    return prev_month


def get_recent_monday(today):
    days_ahead = today.weekday()
    if today.weekday() == 0:
        recent_monday = today
    elif today.weekday() <= 4:
        recent_monday = today + timedelta(days=days_ahead)
    else:
        days_behind = 7 - days_ahead
        recent_monday = today + timedelta(days=days_behind)

    return recent_monday


def get_last_week_dates(today):
    week_end = get_recent_monday(today)
    week_start = week_end - timedelta(days=7)
    week_dates = [week_start + timedelta(days=i) for i in range(8)]
    week_dates_fmt = [day.strftime('%#m/%#d') for day in week_dates]
    return week_dates_fmt
