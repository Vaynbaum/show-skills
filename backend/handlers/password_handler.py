from dotenv import load_dotenv
from passlib.context import CryptContext


class PasswordHandler:
    def __init__(self):
        load_dotenv()
        self.__hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encode_password(self, password: str) -> str:
        """Getting the password hash

        Args:
            password (str): user's password

        Returns:
            str: resulting hash
        """
        return self.__hasher.hash(password)

    def verify_password(self, password: str, encoded_password: str):
        """Checking for a password match

        Args:
            password (str): user's password
            encoded_password (str): password from the database

        Returns:
            bool: True if the password matched the hash, else False
        """
        return self.__hasher.verify(password, encoded_password)
