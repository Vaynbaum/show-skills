from test.data.auth_data import (
    PASSWORD,
    SMIRNOV_EMAIL,
    SMIRNOV_FIRSTNAME,
    SMIRNOV_LASTNAME,
    SMIRNOV_USERNAME,
)


POST_DATA = {
    "name": "test name",
    "url_content": "http://localhost:8000/post/content/post_uml_zgqeuipptbrjwhd.html",
    "skill": {
        "key": "3ed34r43f3",
        "name": "UML-диаграммы",
        "scope": "Программирование",
        "url": "http://localhost:8000/skill/icon/uml.png",
    },
}

POST_EDIT_DATA = {
    "name": "edited name",
    "url_content": "http://localhost:8000/post/content/post_uml_zgqeuipptbrjwhd.html",
    "skill": {
        "key": "3ed34r43f3",
        "name": "UML-диаграммы",
        "scope": "Программирование",
        "url": "http://localhost:8000/skill/icon/uml.png",
    },
}

NO_EXIST_POST_KEY = "no_exist_post_key"
SMIRNOV_REGISTRATION_VALID_DATA = {
    "email": SMIRNOV_EMAIL,
    "username": SMIRNOV_USERNAME,
    "password": PASSWORD,
    "lastname": SMIRNOV_LASTNAME,
    "firstname": SMIRNOV_FIRSTNAME,
}
SMIRNOV_AUTH_VALID_DATA = {"email": SMIRNOV_EMAIL, "password": PASSWORD}
NO_EXIST_SKILL_NAME = "no_exist_name_skill"
