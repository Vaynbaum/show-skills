import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv()
db = Deta(os.getenv("DETA_PROJECT_KEY")).Base("tests")
db.put_many(
    [
        {"followers": [{"name": "Петр",  "lastname": "Петров", "age": 22, "key": "2"}], "lastname": "Иванов", "age": 22, "key": "1"},
        { "followers": [{"name": "Иван","lastname": "Иванов", "age": 22, "key": "1"}], "lastname": "Петров", "age": 22, "key": "2"},
    ]
),
