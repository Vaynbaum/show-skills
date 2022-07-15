from datetime import datetime

from handlers.datetime_handler import DatetimeHandler

datetime_handler = DatetimeHandler()

NO_EXIST_USERNAME = "no_exist_username"

REGISTRATION_ACCOUNT_TO_DELETE = {
    "email": "delete_test@mail.ru",
    "username": "delete_test",
    "password": "qwerty",
    "lastname": "test",
    "firstname": "delete",
}
ACCOUNT_TO_DELETE_AUTH = {
    "email": "delete_test@mail.ru",
    "password": "qwerty",
}
NO_EXIST_KEY_USER = "KEY"


ADDITIONAL_VALID_DATA = {
    "birth_date": datetime_handler.convert_to_int(datetime(1999, 9, 24)),
    "place_residence": "Нижний Новгород",
}
ADDITIONAL_INVALID_DATA = {
    "birth_date": datetime_handler.convert_to_int(datetime(1799, 9, 24)),
    "place_residence": "Нижний Новгород",
}
