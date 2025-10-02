#!/usr/bin/python3
""" Database storage engine """
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """ Interacts with the MySQL database """

    __engine = None
    __session = None

    def __init__(self):
        """ Initialize the connection """
        user = os.getenv('HBNB_MYSQL_USER', 'hbnb_dev')
        pwd = os.getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        db = os.getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')

        self.__engine = create_engine(
                                f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                                pool_pre_ping=True
                                     )

        # Drop all tables if in test environment
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session """
        obj_dict = {}
        classes = [State, City, User, Place, Amenity, Review]

        if cls:
            query_classes = [cls] if isinstance(cls, type) else [cls]
        else:
            query_classes = classes

        for c in query_classes:
            for obj in self.__session.query(c).all():
                key = f"{obj.__class__.__name__}.{obj.id}"
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """ Add object to current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete obj from current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Reloads data from the database """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                                bind=self.__engine, expire_on_commit=False
                                      )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Close the session """
        self.__session.close()
