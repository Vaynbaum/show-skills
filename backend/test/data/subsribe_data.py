from test.data.auth_data import (
    IVANOV_EMAIL,
    IVANOV_FIRSTNAME,
    IVANOV_LASTNAME,
    IVANOV_USERNAME,
    PASSWORD,
)


IVANOV_REGISTRATION_VALID_DATA = {
    "email": IVANOV_EMAIL,
    "username": IVANOV_USERNAME,
    "password": PASSWORD,
    "lastname": IVANOV_FIRSTNAME,
    "firstname": IVANOV_LASTNAME,
}

IVANOV_AUTH_VALID_DATA = {"email": IVANOV_EMAIL, "password": PASSWORD}
