import os
from deta import Deta
from dotenv import load_dotenv

load_dotenv()
db = Deta(os.getenv("DETA_PROJECT_KEY")).Base("messages")
db.put(
    {
        "title": "Добавить навык",
        "content": "Кулинария, приготовление салатов",
        "read": False,
        "completed": False,
    }
)
# db.put_many(
#     [
#         {
#             "followers": [
#                 {"name": "Петр", "lastname": "Петров", "age": 22, "key": "2"}
#             ],
#             "lastname": "Иванов",
#             "age": 23,
#             "key": "1",
#         },
#         {
#             "followers": [
#                 {"name": "Иван", "lastname": "Иванов", "age": 22, "key": "1"}
#             ],
#             "lastname": "Петров",
#             "age": 22,
#             "key": "2",
#         },
#     ]
# ),
# db.update(
#     {"followers": [{"name": "Петр", "lastname": "Петров", "age": 22, "key": "2"}]},
#     "1",
# )

# from calendar import timegm
# from datetime import datetime, timedelta

# # db.put_many(items=[{"key": "2"}, {"key": "1"}], expire_in=10)

# print(timegm(((datetime(2022, 7, 10, 11) + timedelta(minutes=20))).timetuple()))
# result = list(filter(lambda item: "admin" in item["name"], None))
# print(len(result) == 0)
