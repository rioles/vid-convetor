#!/usr/bin/env python
""" holds class User"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from hashlib import md5

class User(BaseModel, Base):
    """ SQLAlchemy User model
    """
    __tablename__ = 'users'

    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)


if __name__=="__main__":
    print(User.__tablename__)

    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))


