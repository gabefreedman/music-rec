#!/usr/bin/env python

from datetime import date
import re

import requests
from bs4 import BeautifulSoup, NavigableString

from dates import get_last_week_dates, get_month


def between(cur, end):
    while cur and cur != end:
        if isinstance(cur, NavigableString):
            text = cur.strip()
            if len(text):
                yield text
        elif str(cur) == '<br/>':
            yield 'gbgfgb'
        cur = cur.next_element


def parse_albums(text):
    pattern = r'\- \d{1,2}\/(\d{1,2}|\?)'
    sep = text.split('gbgfgb')
    sep_text = [re.split(pattern, s) for s in sep]
    sep_text = [item[0] for item in sep_text]
    sep_text = list(filter(None, sep_text))
    return sep_text


def join_soup_text(soup, tag1, tag2):
    if soup.find('b', text=tag1):
        full_text = ''.join(text for text in between(soup.find('b', text=tag1).next_sibling, soup.find('b', text=tag2)))
        full_text = parse_albums(full_text)
    else:
        full_text = []
    return full_text


def main():
    today = date.today()
    month = get_month(today)
    week_dates = get_last_week_dates(today)

    url = f'https://genius.com/Genius-{month}-2019-album-release-calendar-annotated'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'html.parser')

    album_dict = {}
    for i, day in enumerate(week_dates[:-1]):
        album_dict[day] = join_soup_text(soup, week_dates[i], week_dates[i+1])

    return album_dict


if __name__ == '__main__':
    a = main()
