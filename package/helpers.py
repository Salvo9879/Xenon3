
# Import external modules
from flask import Response, redirect, url_for
from flask_login import current_user

import uuid
import datetime

# Variables 
MONTHS_DAY_DATA = {
    'january': 31,
    'february': 29,
    'march': 31,
    'april': 30,
    'may': 31,
    'june': 30,
    'july': 31,
    'august': 30,
    'september': 31,
    'october': 30,
    'november': 31,
    'december': 30
}

MONTH_INDEXED_DATA = [
    'january',
    'february',
    'march',
    'april',
    'may',
    'june',
    'july',
    'august',
    'september',
    'october',
    'november',
    'december',
]

def get_uuid() -> str:
    """ Returns a string universally unique identifier. """
    u = uuid.uuid4()
    return str(u)

def get_dt_now() -> datetime.datetime:
    """ Returns the current datetime. """
    return datetime.datetime.now()

def get_iso_dt(dt: datetime.datetime = None) -> str:
    """ Returns a string of the current datetime in a 8601 ISO format. """
    if dt is None:
        dt = get_dt_now()
    return dt.isoformat()

def get_last_100_years() -> list:
    """ Returns a list of the last 100 years. """
    dt_now = get_dt_now()
    return [dt_now.year - i for i in range(100)]

def get_31() -> list:
    """ Returns a list of numbers between 1 -31. """
    return [i for i in range(1, 32)]

def get_month_names() -> list:
    """ Returns a list of the names of the 12 months. """
    return [m for m in MONTHS_DAY_DATA]