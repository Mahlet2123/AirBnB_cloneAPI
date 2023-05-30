#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from sqlalchemy import create_engine, MetaData, text
from models.base_model import BaseModel, Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
import models
from os import getenv


class DBStorage:
    """DBStorage class"""

    __classNames = [State, City, User, Place, Review, Amenity]

    __engine = None
    __session = None

    def __init__(self):
        """constructor"""
        url = "mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB"),
        )

        self.__engine = create_engine(url, pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            # drop all tables
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """
        query on the current database session (self.__session)
        all objects depending of the class name (argument cls)
        """
        r_dict = {}
        if cls:
            for obj in self.__session.query(cls).all():
                # objs -> list of returned objects
                key = "{}.{}".format(type(obj).__name__, obj.id)
                r_dict[key] = obj
        else:
            for cls in DBStorage.__classNames:
                for obj in self.__session.query(cls).all():
                    # objs -> list of returned objects
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    r_dict[key] = obj
        return r_dict

    def new(self, obj):
        """add the object to the current
        database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current
        database session (self.__session)"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current OOAdatabase session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database (feature of SQLAlchemy)"""
        from sqlalchemy.orm import sessionmaker

        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = Session()

    def classes_dict(self):
        """collection of classes"""

        classes_dict = {
            "BaseModel": BaseModel,
            "State": State,
            "City": City,
            "User": User,
            "Place": Place,
            "Review": Review,
            "Amenity": Amenity
        }
        return classes_dict

    def close(self):
        """
        method on the private session attribute (self.__session)
        """
        self.__session.close()

    def get(self, cls, id):
        """
        method to retrieve one object
        """
        if cls and id:
            if cls in DBStorage.__classNames:
                for obj in self.__session.query(cls).all():
                    if id == obj.id:
                        return obj

    def count(self, cls=None):
        """
        A method to count the number of objects in storage
        """
        count = 0
        count_ = 0
        if cls:
            objs = self.__session.query(cls).all()
            # objs -> list of returned objects
            count = len(objs)
        else:
            for cls in DBStorage.__classNames:
                objs = self.__session.query(cls).all()
                # objs -> list of returned objects
                count_ = len(objs)
                count += count_
        return count
