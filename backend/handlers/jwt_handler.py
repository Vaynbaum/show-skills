import os
from dotenv import load_dotenv
# Используется для кодирования и декодирования токенов json web tokens
import jwt
# Используется для обработки ошибок
from fastapi import HTTPException
# Используется для обработки времени истечения срока действия токенов
from datetime import datetime, timedelta


class JWTHandler():
    def __init__(self):
        load_dotenv()
        self.__secret = os.getenv("APP_SECRET_STRING")
        self.__algorithm = os.getenv("ALGORITHM")
        self.__access_token_expire_minutes = os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES")
        self.__refresh_token_expire_days = os.getenv(
            "REFRESH_TOKEN_EXPIRE_DAYS")

    def encode_token(self, data):
        '''Генерация access токена'''
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=int(self.__access_token_expire_minutes)),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': data
        }
        return jwt.encode(
            payload,
            self.__secret,
            self.__algorithm
        )

    def decode_token(self, token):
        '''Проверка токена'''
        try:
            payload = jwt.decode(token, self.__secret,
                                 algorithms=[self.__algorithm])
            if (payload['scope'] == 'access_token'):
                return payload['sub']
            raise HTTPException(
                status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    # Генерация refresh токена
    def encode_refresh_token(self, data):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=int(self.__refresh_token_expire_days)),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': data
        }
        return jwt.encode(
            payload,
            self.__secret,
            self.__algorithm
        )

    def refresh_token(self, refresh_token):
        '''Создание нового access токена по refresh токену'''
        try:
            payload = jwt.decode(
                refresh_token, self.__secret, algorithms=[self.__algorithm])
            if (payload['scope'] == 'refresh_token'):
                data = payload['sub']
                new_token = self.encode_token(data)
                return new_token
            raise HTTPException(
                status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=401, detail='Invalid refresh token')
