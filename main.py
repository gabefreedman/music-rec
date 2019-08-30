#!/usr/bin/env python

"""This module contains code for doing core HTML requests and
parsing into tabular format. Main function will generate
MultiIndex DataFrame and call send_email function to send
the data via email. I personally choose to schedule this script
to run weekly.

"""

from datetime import date
import re
from itertools import groupby
import operator

import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd

from dates import get_last_week_dates
from mail import send_email


def between(cur, end):
    """Collect text between HTML tag and given ending string.

    Creates one long string containing all text (not including
    string representations of HTML tags) from a given HTML tag
    up to but not including a given ending string.

    Parameters
    ----------
    cur : bs4.Tag
        tag
    end : str
        String on which to end search through HTML snippet.
    Returns
    -------
    contents : list of str
        Contains email login credentials as [user, pass]

    """
    while cur and not str(cur).startswith(end):
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if text:
                yield text
        elif str(cur) == '<br/>':
            yield 'gbgfgb'
        cur = cur.next_element


def parse_albums(text):
    """Parses string containing album and artists text information.

    Creates one long string containing all text (not including
    string representations of HTML tags) from a given HTML tag
    up to but not including a given ending string.

    Parameters
    ----------
    text : str
        String containing artist and album names to be separated.

    Returns
    -------
    final_text : list of str
        Each element of list is artist name and album name separated
        by ----.

    """
    pattern = r'\- \d{1,2}\/(\d{1,2}|\?)'
    sep = text.split('gbgfgb')
    sep_text = [re.split(pattern, s) for s in sep]
    sep_text = [item[0] for item in sep_text]
    sep_text = list(filter(None, sep_text))

    parsed = [s.split('-') for s in sep_text]
    parsed = [[s.strip() for s in s1] for s1 in parsed]
    final_text = [s[0] + '  ----  ' + s[1] for s in parsed]

    return final_text


def join_soup_text(soup, tag1):
    end_of_month = ['1/31', '2/28', '3/31', '4/30', '5/31', '6/30',
                    '7/31', '8/31', '9/30', '10/31', '11/30', '12/31']

    if soup.find('b', text=tag1):
        if tag1 in end_of_month:
            full_text = ''.join(text for text in between(soup.find('b', text=tag1).next_sibling,
                                                         end='<div>'))
        else:
            full_text = ''.join(text for text in between(soup.find('b', text=tag1).next_sibling,
                                                         end='<b>'))
        full_text = parse_albums(full_text)
    else:
        full_text = []
    return full_text


def generate_album_data(week_dates):
    month = week_dates[0][1]
    dates = [week_dates[i][0] for i in range(len(week_dates))]
    url = f'https://genius.com/Genius-{month}-2019-album-release-calendar-annotated'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    album_dict = {}
    for i, day in enumerate(dates[:-1]):
        album_dict[day] = join_soup_text(soup, dates[i])

    return album_dict


def parse_album_dictionary(album_dict):
    col_split = {}
    for key, value in album_dict.items():
        col_split[key] = [s.split(' ---- ') for s in value]

    multi_df = {}
    for key, value in col_split.items():
        multi_df[key] = pd.DataFrame(value, columns=['Artist', 'Album/EP Title'])
        multi_df[key] = multi_df[key].set_index('Artist')
        multi_df[key].columns.name = multi_df[key].index.name
        multi_df[key].index.name = None

    parsed_df = pd.concat(multi_df.values(), keys=multi_df.keys())
    return parsed_df


def generate_album_dictionary(week_dates):
    group_months = [list(group) for key, group in groupby(week_dates, operator.itemgetter(1))]
    if len(group_months) == 2:
        month1 = group_months[0]
        month1.append(('NONE', month1[0][1]))
        month2 = group_months[1]

        albums1 = generate_album_data(month1)
        albums2 = generate_album_data(month2)
        album_dict = {**albums1, **albums2}
    else:
        album_dict = generate_album_data(week_dates)

    return album_dict


def main():
    """Main function for generating data and sending email."""
    today = date.today()
    week_dates = get_last_week_dates(today)
    album_dict = generate_album_dictionary(week_dates)

    album_df = parse_album_dictionary(album_dict)

    send_email(album_df)


if __name__ == '__main__':
    main()
