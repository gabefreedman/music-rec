#!/usr/bin/env python

"""This module defines functions for manipulating and formatting date
and datetime objects.

"""

from datetime import timedelta


def get_month(today):
    """Format datetime to string variable of month name.

    Takes in `today` and extracts the full month
    name. The name is returned in all lowercase so
    as to match the name of the URL.

    Parameters
    ----------
    today : datetime object

    Returns
    -------
    month : str
        Full name month extracted from datetime input.

    """
    month = today.strftime('%B').lower()
    return month


def get_previous_month(today):
    """Get full name of last month given datetime object.

    Takes in `today` and finds the date of the last
    day of the previous month. Formatted so as to
    match the URL.

    Parameters
    ----------
    today : datetime object

    Returns
    -------
    prev_month : str
        Full name of last month extracted from datetime
        input.

    """
    first_of_month = today.replace(day=1)
    prev = first_of_month - timedelta(days=1)
    prev_month = prev.strftime('%B').lower()
    return prev_month


def get_recent_monday(today):
    """Find the date of the nearest Monday.

    Takes in `today` and and extracts the full month
    name. The name is returned in all lowercase so
    as to match the name of the URL.

    Parameters
    ----------
    today : datetime object

    Returns
    -------
    recent_monday : date object
        Date of nearest Monday to input datetime

    """
    days_ahead = today.weekday()
    if today.weekday() == 0:
        recent_monday = today
    elif today.weekday() <= 4:
        recent_monday = today - timedelta(days=days_ahead)
    else:
        days_behind = 7 - days_ahead
        recent_monday = today + timedelta(days=days_behind)

    return recent_monday


def get_last_week_dates(today):
    """Retrieve the dates of the past 8 days.

    Generates a list of dates in {month#}/{year#}
    format from the past Monday to nearest Monday, inclusive.
    Merges with full month name to form tuples.

    Parameters
    ----------
    today : datetime object

    Returns
    -------
    full_week : list of 2-tuples
        2-tuple of the form: (weekdate, full month name)

    """
    week_end = get_recent_monday(today)
    week_start = week_end - timedelta(days=7)

    week_dates = [week_start + timedelta(days=i) for i in range(8)]
    week_dates_fmt = [day.strftime('%#m/%#d') for day in week_dates]
    months = [get_month(day) for day in week_dates]
    full_week = list(zip(week_dates_fmt, months))
    return full_week
