import jwt, datetime, os
from flask import Flask, request
#from models.hello import hello
from models.engine.db_storage import DBStorage
from models.user import User
from utils import HashAndEncriptPassword
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Union
from bcrypt import hashpw, gensalt, checkpw
#from api.app import hello

def hey():
    print("hello woor")



class Auth:

    def __init__(self):
        self.__storage = DBStorage()

    def register_user(self, **kwargs):
        """ User registration
		"""

        email = ""
        password = ""

        self.__storage.reload()
        
        for key, value in kwargs.items():
            if key == "email":
                email = kwargs[key]
            elif key == "hashed_password":
                password = kwargs[key]
        users_found = self.__storage.find_user_by(email=email)
        print(f"out try {users_found}")
        try:
            users_found = self.__storage.find_user_by(email=email)
            print(f"in try {users_found}")
            if users_found:
                return print("User {} already exists".format(email))
                #raise ValueError("User {} already exists".format(email)) 
            else:
                kwargs["hashed_password"] = HashAndEncriptPassword.hash_password(password).decode('utf-8')
                user = User(**kwargs)
                user.email = kwargs["email"]
                user.hashed_password = kwargs["hashed_password"]
                print(user)
                self.__storage.new(user)
                self.__storage.save()
                return user       
        except NoResultFound: 
            pass

    def valid_login(self, obj: User) -> bool:
        """ Login validation
        """
        self.__storage.reload()
        if not obj.email or not obj.hashed_password:
            return False
        try:
            users_found = self.__storage.find_user_by(email=obj.email)
            hashed_password = users_found.hashed_password
            return checkpw(obj.hashed_password.encode(),
                           hashed_password.encode('utf-8'))
        except (NoResultFound, InvalidRequestError):
            return False

    def create_jwt(self, **kwargs):
        return jwt.encode(
            {
                "usernam": kwargs["email"],
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                + datetime.timedelta(days=1),
                "iat": datetime.datetime.utcnow(),
                "admin": kwargs["authz"],
            },
            kwargs["secret"],
            algorithm="HS256",
        )
    @staticmethod
    def say_hell():
        print("hello mum")
if __name__ =="__main__":
    mydict = HashAndEncriptPassword.get_user_data()
    print(mydict)

    au = Auth()
    u = User(**mydict)
    #storage = DBStorage()
    #storage.reload()
    #print(storage)
    #u = au.register_user(**mydict)
    print(au.valid_login(u))
    


