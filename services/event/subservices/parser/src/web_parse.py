import requests
from bs4 import BeautifulSoup
from fastapi import UploadFile
from pandas import DataFrame

from src.services.event.subservices.parser.src.punching_systems.SFR_parse import SFR_parsing
from src.services.event.subservices.parser.src.punching_systems.SPORT_ORG_parse import SO_parsing
from src.services.event.subservices.parser.src.punching_systems.WinOrient_parse import SI_parsing
from src.services.event.subservices.parser.src.punching_systems.utils import bs


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


def get_source(source_link: str, source_file: UploadFile) -> BeautifulSoup:
    if source_link:
        return web_parse(source_link)
    else:
        return file_parse(source_file)


