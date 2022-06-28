# Используется для хеширования пароля
from dotenv import load_dotenv
from passlib.context import CryptContext


class PasswordHandler():
    def __init__(self):
        load_dotenv()
        self.__hasher = CryptContext(
            schemes=["bcrypt"], deprecated="auto")

    def encode_password(self, password):
        '''Получение хэша пароля'''
        return self.__hasher.hash(password)

    def verify_password(self, password, encoded_password):
        '''Проверка совпадения паролей'''
        return self.__hasher.verify(password, encoded_password)
