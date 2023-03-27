import models
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from models.user import User
Base = declarative_base()

class DBStorage:
    """interaacts with the MySQL database"""
    __engine = ""
    __session = ""


    def __init__(self):
        """Instantiate a DBStorage object"""
        VICO_MYSQL_USER = getenv('VICO_MYSQL_USER')
        VICO_MYSQL_PWD = getenv('VICO_MYSQL_PWD')
        VICO_MYSQL_HOST = getenv('VICO_MYSQL_HOST')
        VICO_MYSQL_DB = getenv('VICO_MYSQL_DB')
        VICO_MYSQL_PORT = getenv('VICO_MYSQL_PORT')
        self.__engine = create_engine(f"mysql+mysqldb://{VICO_MYSQL_USER}:{VICO_MYSQL_PWD}@{VICO_MYSQL_HOST}/{VICO_MYSQL_DB}")

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
        print(self.__session)
   
    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)
        print(f"{self.__session.add(obj)} this is object a")

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by the given criteria
        Args:
            **kwargs: The criteria to search for
        Returns:
            User: The found user
        """
        user = self.__session.query(User).filter_by(**kwargs).first()
        if not user:
            return 0
        else:
            return user
   
    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update the given user
        Args:
            user_id (int): The id of the user to update
            **kwargs: The fields to update
        Returns:
            None
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise InvalidRequestError
            self._session.commit()
        except (NoResultFound, InvalidRequestError, ValueError):
            raise

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
