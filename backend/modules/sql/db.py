from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import *

# Создание строки подключения
DATABASE_URL: str = f'{Dialect}://{Username}:{Password}@{Host}:{Port}/{Database}'
# Создание движка
engine = create_engine(DATABASE_URL)
# Создание сессии для взаимодействия с базой данных
session = sessionmaker( bind=engine)
# Создание декларативного базового класса для создания моделей
Base = declarative_base()