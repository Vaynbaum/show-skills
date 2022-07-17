from test.data.auth_data import (
    PASSWORD,
    SMIRNOV_EMAIL,
    SMIRNOV_FIRSTNAME,
    SMIRNOV_LASTNAME,
    SMIRNOV_USERNAME,
)


POST_DATA = {
    "name": "test name",
    "content_html": "<p>test content<img alt='' src='http://localhost:8000/post/photo/qxyzxrtz_%D0%91%D0%B0%D0%B7%D0%B0%D0%94%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.png' style='width:567px' /></p>",
    "skill": {
        "key": "3ed34r43f3",
        "name": "UML-диаграммы",
        "scope": "Программирование",
        "url": "http://localhost:8000/skill/icon/uml.png",
    },
}

POST_EDIT_DATA = {
    "name": "edited name",
    "content_html": "<p>test content<img alt='' src='http://localhost:8000/post/photo/qxyzxrtz_%D0%91%D0%B0%D0%B7%D0%B0%D0%94%D0%B0%D0%BD%D0%BD%D1%8B%D1%85.png' style='width:567px' /></p>",
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
