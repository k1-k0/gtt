import asyncio
from collections import namedtuple
from typing import List
import json

import requests
from bs4 import BeautifulSoup


DOMAIN = "https://play.google.com"

ApplicationInfo = namedtuple('ApplicationInfo',
                             ['name', 'url', 'author', 'category',
                              'description', 'average_rating',
                              'review_count', 'last_update'])


def transform_to_query(name: str):
    return name.replace(' ', '+')


def validate_applications(apps_info: List[ApplicationInfo], keyword: str):
    validated = []
    for app_info in apps_info:
        if validate_application_info(app_info=app_info, keyword=keyword):
            validated.append(app_info)
    return validated


def validate_application_info(app_info: ApplicationInfo, keyword: str):
    validated = False
    if name := app_info.name:
        validated = keyword in name.lower()
    if not validated and app_info.description:
        validated = keyword in app_info.description.lower()

    return validated


def convert_applications_info_to_json(apps_info: List[ApplicationInfo]):
    container = []
    for app_info in apps_info:
        obj = {
            "Name": app_info.name,
            "URL": app_info.url,
            "Author": app_info.author,
            "Category": app_info.category,
            "Description": app_info.description,
            "Average_rating": app_info.average_rating,
            "Review_count": app_info.review_count,
            "Last_update": app_info.last_update,
        }
        container.append(obj)

    if len(container) == 1:
        return json.dumps(container[0], ensure_ascii=False)

    return json.dumps(obj, ensure_ascii=False)

def get_application_links(name: str):
    """Get list of links to similar applications"""

    # Making a GET request
    query = transform_to_query(name)
    url=f'{DOMAIN}/store/search?q={query}%20app'
    request = requests.get(url)

    # Parsing the search page
    soup = BeautifulSoup(request.content, 'html.parser')
    application_cards = soup.find_all("div", class_="ULeU3b")

    application_links = []
    for application_card in application_cards:
        link = application_card.find("a", class_="Si6A0c Gy4nib")
        if link:
            application_link = ''.join((DOMAIN, link["href"]))
            application_links.append(application_link)

    return application_links


async def parse_application_page(application_link: str) -> ApplicationInfo:
    """Get needed information of application from page"""
    request = requests.get(application_link)
    soup = BeautifulSoup(request.content, "html.parser")

    results = await asyncio.gather(
        get_app_name(soup),
        get_app_author(soup),
        get_app_category(soup),
        get_app_description(soup),
        get_app_average_rating(soup),
        get_app_review_count(soup),
        get_app_last_update(soup)
    )

    if results:
        app_info = ApplicationInfo(
            name=results[0],
            url=application_link,
            author=results[1],
            category=results[2],
            description=results[3],
            average_rating=results[4],
            review_count=results[5],
            last_update=results[6],
        )

    return app_info


async def get_app_name(soup: BeautifulSoup) -> str:
    name = soup.find("h1", class_="Fd93Bb")
    return name.text if name else None

async def get_app_author(soup: BeautifulSoup) -> str:
    author = soup.find("div", class_="Vbfug auoIOc")
    return author.text if author else None

async def get_app_category(soup: BeautifulSoup) -> str:
    category = soup.find("div", class_="Uc6QCc")
    if category:
        return category.text if category else None

async def get_app_description(soup: BeautifulSoup) -> str:
    description = soup.find("div", class_="bARER")
    if description:
        return description.text if description else None

async def get_app_average_rating(soup: BeautifulSoup) -> str:
    average_rating = soup.find("div", class_="jILTFe")
    return average_rating.text if average_rating else None

async def get_app_review_count(soup: BeautifulSoup) -> str:
    review_count = soup.find("div", class_="EHUI5b")
    if review_count:
        numeric_part = review_count.text.split()[0]
        return numeric_part

async def get_app_last_update(soup: BeautifulSoup) -> str:
    last_update = soup.find("div", class_="xg1aie")
    return last_update.text if last_update else None
