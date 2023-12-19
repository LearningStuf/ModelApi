import os
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import logging.config

project_path = Path(__file__).resolve().parent.parent
path_config = project_path / "config"


custom_logger = logging.getLogger()

class AuthHandler():
    '''
    The class handles the logic for encoding and deconding the jwt token\n
    The class also has the methods to hash the password form plain text to store it
    in the sqlite, and also to authenticate the user.
    '''
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    load_dotenv(dotenv_path=path_config / ".env")
    secret = os.getenv("JWT_SECRET_KEY")

    def get_password_hash(self, password):
        '''
        The function hashes the password.
        :param password: The plaintext password that needs to be hased to be stored in sqlite
        '''
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        '''
        The function takes in both the plain text password and the hased password to verify the credentials
        :param plain_password: The plain password
        :param hashed_password: The hashed password stored in the db
        '''
        return self.pwd_context.verify(plain_password, hashed_password)

    def encode_token(self, user_id):
        '''
        The function encodes the username in a jwt token utilizing the secret. The jwt token will have an expiry
        of certian minutes mentions in the config file. The function will return the jwt token.
        :param user_id: The username sent in the request
        '''

        payload = {
            'exp': datetime.utcnow() + timedelta(minutes = float(os.getenv("JWT_EXPIRY_IN_MINIUTES"))),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    def decode_token(self, token):
        '''
        The function will be utilized to decode the jwt token.
        The function will also be responsible to give http errors if the token is expired or invalid
        This function will be called by auth_wrapper function to decode the jwt, do not call it directly

        :param token: The JWT token that needs to be decoded.
        '''
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            custom_logger.error("JWT token for the request has expired ")
            raise HTTPException(status_code=401, detail='Signature has expired')
        except jwt.InvalidTokenError as e:
            custom_logger.error(f"Invalid toke was provided for the request {e}")
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        '''
        Add this function at your end point as a dependency so that you can enable authorization
        funtionality for your endpoint.
        '''
        return self.decode_token(auth.credentials)