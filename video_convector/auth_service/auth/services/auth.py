import jwt, datetime, os
from flask import Flask, request
#from models.hello import hello
from models.engine.db_storage import DBStorage
from models.user import User
#from utils import HashAndEncriptPassword
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Union
from bcrypt import hashpw, gensalt, checkpw

print(("okay"))