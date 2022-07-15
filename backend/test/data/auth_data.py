PASSWORD = "secret"

IVANOV_LASTNAME = "Иван"

IVANOV_FIRSTNAME = "Иванов"

IVANOV_USERNAME = "ivanov_test"

IVANOV_EMAIL = "ivanov_test@mail.ru"
IVANOV1_EMAIL = "ivanov1_test@mail.ru"
PETROV_EMAIL = "petrov_test@mail.ru"


IVANOV1_REGISTRATION_INVALID_DATA = {
    "email": IVANOV1_EMAIL,
    "username": IVANOV_USERNAME,
    "password": PASSWORD,
    "lastname": IVANOV_FIRSTNAME,
    "firstname": IVANOV_LASTNAME,
}
IVANOV_REGISTRATION_VALID_DATA = {
    "email": IVANOV_EMAIL,
    "username": IVANOV_USERNAME,
    "password": PASSWORD,
    "lastname": IVANOV_FIRSTNAME,
    "firstname": IVANOV_LASTNAME,
}

IVANOV_AUTH_VALID_DATA = {"email": IVANOV_EMAIL, "password": PASSWORD}
IVANOV_AUTH_INVALID_DATA = {"email": IVANOV_EMAIL, "password": PASSWORD + "32"}
PETROV_AUTH_VALID_DATA = {"email": PETROV_EMAIL, "password": PASSWORD}
