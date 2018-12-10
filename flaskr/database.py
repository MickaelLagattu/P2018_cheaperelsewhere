import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from flask_pymongo import PyMongo

class DatabaseNotInitializedException(Exception):
    pass

class Database():
    """Class to interact with database"""

    def __init__(self, app):
        """Constructor"""
        app.config['MONGO_URI'] = "mongodb://localhost:27017/myDatabase"
        self.__mongo = PyMongo(app)

    @property
    def mongo(self):
        """Returns the mongodb database"""
        return self.__mongo