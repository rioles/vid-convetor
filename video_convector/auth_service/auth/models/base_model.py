#!/usr/bin/env python
import sqlalchemy
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import uuid
from typing import TypeVar, List, Iterable
from os import path
from datetime import datetime
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
import models
Base = declarative_base()
import utils

class BaseModel:
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """Initialization of the base model"""
        if kwargs:
            self.id = str(uuid.uuid4())
            for key, value in kwargs.items():
                if key != "__class__":
                    self.__dict__[key] = value
                if kwargs.get("created_at", None) and type(self.created_at) is str:
                    self.created_at = datetime.strptime(kwargs["created_at"], TIMESTAMP_FORMAT)
                else:
                    self.created_at = datetime.utcnow()

                if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                    self.updated_at = datetime.strptime(kwargs["updated_at"], TIMESTAMP_FORMAT)
                else:
                    self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self)-> str:
        classe_name = self.__class__.__name__
        return f"[{classe_name}] ({self.id}) {self.__dict__}"

    def save(self) -> None:
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()


if __name__=="__main__":
    my_model = BaseModel()
    my_model.name = "My First Model"
    my_model.my_number = 89
    print(my_model)
    #dico = my_model.new(my_model)
    #print(my_model.__str__())
