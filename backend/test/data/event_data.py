from datetime import datetime
from consts.name_format_event import OFFLINE, ONLINE
from handlers.datetime_handler import DatetimeHandler
from test.data.auth_data import (
    IVANOV_EMAIL,
    IVANOV_FIRSTNAME,
    IVANOV_LASTNAME,
    IVANOV_USERNAME,
    PASSWORD,
    PETROV_EMAIL,
    PETROV_FIRSTNAME,
    PETROV_LASTNAME,
    PETROV_USERNAME,
    SMIRNOV_EMAIL,
    SMIRNOV_FIRSTNAME,
    SMIRNOV_LASTNAME,
    SMIRNOV_USERNAME,
    SOBOLEV_EMAIL,
    SOBOLEV_FIRSTNAME,
    SOBOLEV_LASTNAME,
    SOBOLEV_USERNAME,
)


datetime_handler = DatetimeHandler()
EVENT_VALID_DATA = {
    "name": "Вебинар по Angular",
    "date": datetime_handler.now_next_days(2),
    "format_event": ONLINE,
    "place": {"name_platform": "VK", "URL": "https://example"},
}

EVENT_EDIT_VALID_DATA = {
    "name": "Вебинар по Angular",
    "date": datetime_handler.now_next_days(2),
    "format_event": OFFLINE,
    "place": {"zoom": 19, "position": {"lat": 56.326794, "lng": 44.025554}},
}

EVENT_INVALID_DATA = {
    "name": "Вебинар по Angular",
    "date": datetime_handler.convert_to_int(datetime(2017, 10, 12, 12)),
    "format_event": OFFLINE,
    "place": {"zoom": 19, "position": {"lat": 56.326794, "lng": 44.025554}},
}
NO_EXIST_EVENT_KEY = "no_exist_event_key"
IVANOV_REGISTRATION_VALID_DATA = {
    "email": IVANOV_EMAIL,
    "username": IVANOV_USERNAME,
    "password": PASSWORD,
    "lastname": IVANOV_FIRSTNAME,
    "firstname": IVANOV_LASTNAME,
}
PETROV_REGISTRATION_VALID_DATA = {
    "email": PETROV_EMAIL,
    "username": PETROV_USERNAME,
    "password": PASSWORD,
    "lastname": PETROV_FIRSTNAME,
    "firstname": PETROV_LASTNAME,
}
SMIRNOV_REGISTRATION_VALID_DATA = {
    "email": SMIRNOV_EMAIL,
    "username": SMIRNOV_USERNAME,
    "password": PASSWORD,
    "lastname": SMIRNOV_LASTNAME,
    "firstname": SMIRNOV_FIRSTNAME,
}
SOBOLEV_REGISTRATION_VALID_DATA = {
    "email": SOBOLEV_EMAIL,
    "username": SOBOLEV_USERNAME,
    "password": PASSWORD,
    "lastname": SOBOLEV_LASTNAME,
    "firstname": SOBOLEV_FIRSTNAME,
}
IVANOV_AUTH_VALID_DATA = {"email": IVANOV_EMAIL, "password": PASSWORD}
PETROV_AUTH_VALID_DATA = {"email": PETROV_EMAIL, "password": PASSWORD}
SMIRNOV_AUTH_VALID_DATA = {"email": SMIRNOV_EMAIL, "password": PASSWORD}
SOBOLEV_AUTH_VALID_DATA = {"email": SOBOLEV_EMAIL, "password": PASSWORD}