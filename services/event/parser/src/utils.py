# -*- coding: utf-8 -*-
import re
from typing import Union

import pandas as pd
import requests
from bs4 import BeautifulSoup as BS, BeautifulSoup
from fastapi import UploadFile
from pandas import Timedelta, DataFrame
from pandas._libs import NaTType

from src.services.event.parser.src.punching_systems.SFR_parse import SFR_parsing
from src.services.event.parser.src.punching_systems.SPORT_ORG_parse import SO_parsing
from src.services.event.parser.src.punching_systems.WinOrient_parse import SI_parsing


def bs(s: BS):
    soup: BS = BS(str(s), 'html.parser')
    return soup


def course(l: list):
    r = range(len(l) - 1)
    f = lambda x: re.sub(r', ', '->', str(x))[1:-1]
    return [f(l[i:i + 2]) for i in r]


null: Union[Timedelta, NaTType, NaTType] = Timedelta(seconds=0)


def points_to_routes(l: list):
    f = lambda x, i: (int(x[i]), int(x[i + 1]))
    l: list = [f(l, i) for i in range(len(l) - 1)]
    return l


def rl(l: list):
    return range(len(l))


def fill_GD(names, points_l, splits_l, results):
    GD = {}
    for name in names:
        try:
            sportsman_info = routes_and_splits_dict(points_l[name], splits_l[name])
        except ValueError:
            # print(len(points_l[name]),splits_l[name])
            sportsman_info = {}
        sportsman_info.setdefault('RES', results[name])
        GD.setdefault(name, sportsman_info)
    return GD


def routes_and_splits_dict(routes: list, splits: list):
    if len(routes) == len(splits):
        d: dict = dict(zip(routes, splits))
        return d
    else:
        raise ValueError(f'{len(routes), len(splits)} lenghts arent same')


def dispersions(d: dict):
    disp = {k: {leg: n for n, leg in enumerate(v)} for k, v in d.items()}
    return pd.DataFrame(disp).T


def get_source(source_link: str, source_file: UploadFile) -> BeautifulSoup:
    if source_link:
        return web_parse(source_link)
    else:
        return file_parse(source_file)


def parse_event(page: BeautifulSoup) -> (DataFrame, DataFrame):
    title = str(page.find('title'))
    if 'WinOrient' in title:
        return SI_parsing(page)
    elif 'SportOrg' in title:
        return SO_parsing(page)
    else:
        return SFR_parsing(page)


def web_parse(link: str) -> BeautifulSoup:
    content = ''
    if 'http' in link:
        response = requests.get(link)
        try:
            content = response.content.decode(response.apparent_encoding)
        except UnicodeEncodeError as e:
            content = ''
    soup_page = bs(content)
    return soup_page


def file_parse(data: bytes) -> BeautifulSoup:
    pass
