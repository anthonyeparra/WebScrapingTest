from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool
from os import environ

class DataBase():

    base_class = declarative_base()  # Extend class for models

    def __init__(self):

        # Get connections strings from secret manager
        connection_strings = self.__get_connection_strings()

        string_connection = connection_strings

        # Create a engine DB
        self.__engine = create_engine(string_connection, poolclass=QueuePool)
        # Create the association between the engine and the session
        self.__session_maker = sessionmaker(bind=self.__engine)
        # Create a new session
        self.session = self.__session_maker()

    def __get_connection_strings(self):

        read_string = "mysql+pymysql://{0}:{1}@{2}/{3}".format(
            environ.get('DB_USER'),
            environ.get('DB_PASSWORD'),
            environ.get('DB_HOST'),
            environ.get('DB_NAME')
        )

        return read_string
