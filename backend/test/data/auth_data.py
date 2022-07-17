PASSWORD = "secret"

IVANOV_LASTNAME = "Иван"
PETROV_LASTNAME = "Петров"
SMIRNOV_LASTNAME = "Смирнов"
SOBOLEV_LASTNAME = "Соболев"

IVANOV_FIRSTNAME = "Иванов"
PETROV_FIRSTNAME = "Петр"
SMIRNOV_FIRSTNAME = "Александр"
SOBOLEV_FIRSTNAME = "Алексей"

IVANOV_USERNAME = "ivanov_test"
PETROV_USERNAME = "petrov_test"
SMIRNOV_USERNAME = "smirnov_test"
SOBOLEV_USERNAME = "sobolev_test"

IVANOV_EMAIL = "ivanov_test@mail.ru"
IVANOV1_EMAIL = "ivanov1_test@mail.ru"
PETROV_EMAIL = "petrov_test@mail.ru"
SMIRNOV_EMAIL = "smirnov_test@mail.ru"
SOBOLEV_EMAIL = "sobolev_test@mail.ru"

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
