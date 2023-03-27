from bcrypt import hashpw, gensalt, checkpw
from os import getenv
class HashAndEncriptPassword:
    @staticmethod
    def hash_password(password: str) -> bytes:
        """ Hash password
        """
        return hashpw(password.encode(), gensalt())

    @staticmethod
    def get_user_data():
        my_hash = {}
        email =  getenv('email')
        hashed_password = getenv('hashed_password')
        my_hash["email"] = email
        my_hash["hashed_password"] = hashed_password
        return my_hash

    @staticmethod
    def get_user_jwt():
        JWT_SECRET = getenv('JWT_SECRET')
        return JWT_SECRET


    
    