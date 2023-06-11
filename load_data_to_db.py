from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, date

import schedule as schedule
from sqlalchemy.orm import Session
from time import sleep
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from db import models
from db.engine import Base, engine

BASE_URL = "https://www.oree.com.ua/index.php/PXS/get_pxs_hdata/"

current_date = datetime.now().date()
information_date = current_date + timedelta(days=1)
market_data_url = urljoin(BASE_URL, f"{information_date.strftime('%d.%m.%Y')}/DAM/2")


@dataclass
class Pricing:
    date: date
    hour: int
    price: float
    volume: float


def parse_one_hour_data(hour_soup: BeautifulSoup) -> Pricing:
    """
    Get data from BeautifulSoup and Create instance of class Prising

    """
    return Pricing(
        date=information_date,
        hour=int(hour_soup.select("td")[1].text.split()[1]),
        price=float(hour_soup.select("td")[2].text.split()[1]),
        volume=float(hour_soup.select("td")[3].text.split()[1])
    )


def get_data(url: str) -> list[Pricing]:
    """
    Functions takes url for parsing data and return list Pricing class instances
    """
    response = requests.get(url, verify=False).content
    soup = BeautifulSoup(response, "html.parser")
    hourly_prices = soup.find("tbody").select("tr")
    prices = [parse_one_hour_data(elem) for elem in hourly_prices]
    return prices


def write_data_to_db(pricing_list: list[Pricing]) -> None:
    """
    Function takes list of Pricinf instances and load them to db
    """
    with Session(autoflush=False, bind=engine) as db:
        for obj in pricing_list:
            one_hour_price = models.DBPricing(
                date=obj.date,
                hour=obj.hour,
                price=obj.price,
                volume=obj.volume
            )
            db.add(one_hour_price)
        db.commit()


def one_day_loading() -> None:
    """
    This functon get data from url and loads it to db, if data is not available yet, it tries it after minute
    """
    while True:
        try:
            pricing_list = get_data(market_data_url)

            write_data_to_db(pricing_list)
            print("Data was loaded to db")
            break
        except AttributeError:
            print("Data fot next day is not available yet")
            sleep(60)


schedule.every().day.at("12:00").do(one_day_loading)

while True:
    schedule.run_pending()
    sleep(1)
