import os
from dotenv import load_dotenv
import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta

from consts.name_tokens import ACCESS_TOKEN, REFRESH_TOKEN


class JWTHandler:
    def __init__(self):
        load_dotenv()
        self.__secret = os.getenv("APP_SECRET_STRING")
        self.__algorithm = os.getenv("ALGORITHM")
        self.__access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        self.__refresh_token_expire_days = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

    def __generate_token(self, key: str, type: str, expiration: timedelta) -> str:
        """Private method generating a token

        Args:
            key (str): user's key in the database
            type (str): token type
            expiration (timedelta): token lifetime

        Returns:
            str: generated token
        """
        payload = {
            "exp": datetime.utcnow() + expiration,
            "iat": datetime.utcnow(),
            "scope": type,
            "sub": key,
        }
        return jwt.encode(payload, self.__secret, self.__algorithm)

    def encode_token(self, key: str) -> str:
        """Generating access token

        Args:
            key (str): user's key in the database

        Returns:
            str: generated access token
        """
        return self.__generate_token(
            key,
            ACCESS_TOKEN,
            timedelta(minutes=int(self.__access_token_expire_minutes)),
        )

    def decode_token(self, token: str) -> str:
        """Getting a subject from a token

        Args:
            token (str)

        Raises:
            HTTPException: If the token is invalid, expired or scope is invalid

        Returns:
            str: Information stored in subject
        """
        try:
            payload = jwt.decode(token, self.__secret, algorithms=[self.__algorithm])
            if payload["scope"] == ACCESS_TOKEN:
                return payload["sub"]
            raise HTTPException(
                status_code=401, detail="Scope for the token is invalid"
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def encode_refresh_token(self, key: str) -> str:
        """Generating refresh token

        Args:
            key (str): user's key in the database

        Returns:
            str: generated refresh token
        """
        return self.__generate_token(
            key, REFRESH_TOKEN, timedelta(days=int(self.__refresh_token_expire_days))
        )

    def refresh_token(self, refresh_token: str) -> str:
        """Creating a new access token by refresh token

        Args:
            refresh_token (str)

        Raises:
            HTTPException: If the refresh token is invalid, expired or scope is invalid
        Returns:
            str: new access token
        """
        try:
            payload = jwt.decode(
                refresh_token, self.__secret, algorithms=[self.__algorithm]
            )
            if payload["scope"] == REFRESH_TOKEN:
                data = payload["sub"]
                new_token = self.encode_token(data)
                return new_token
            raise HTTPException(status_code=401, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
