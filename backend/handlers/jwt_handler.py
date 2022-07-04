import os
from dotenv import load_dotenv

# Используется для кодирования и декодирования токенов json web tokens
import jwt

# Используется для обработки ошибок
from fastapi import HTTPException

# Используется для обработки времени истечения срока действия токенов
from datetime import datetime, timedelta


class JWTHandler:
    def __init__(self):
        load_dotenv()
        self.__secret = os.getenv("APP_SECRET_STRING")
        self.__algorithm = os.getenv("ALGORITHM")
        self.__access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        self.__refresh_token_expire_days = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

    def __generate_token(self, key: str, type: str, offset: timedelta):
        """Приватная генерация токена"""
        payload = {
            "exp": datetime.utcnow() + offset,
            "iat": datetime.utcnow(),
            "scope": type,
            "sub": key,
        }
        return jwt.encode(payload, self.__secret, self.__algorithm)

    def encode_token(self, key):
        """Генерация access токена"""
        return self.__generate_token(
            key,
            "access_token",
            timedelta(minutes=int(self.__access_token_expire_minutes)),
        )

    def decode_token(self, token):
        """Проверка токена"""
        try:
            payload = jwt.decode(token, self.__secret, algorithms=[self.__algorithm])
            if payload["scope"] == "access_token":
                return payload["sub"]
            raise HTTPException(
                status_code=401, detail="Scope for the token is invalid"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def encode_refresh_token(self, key):
        """Генерация refresh токена"""
        return self.__generate_token(
            key, "refresh_token", timedelta(days=int(self.__refresh_token_expire_days))
        )

    def refresh_token(self, refresh_token):
        """Создание нового access токена по refresh токену"""
        try:
            payload = jwt.decode(
                refresh_token, self.__secret, algorithms=[self.__algorithm]
            )
            if payload["scope"] == "refresh_token":
                data = payload["sub"]
                new_token = self.encode_token(data)
                return new_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
