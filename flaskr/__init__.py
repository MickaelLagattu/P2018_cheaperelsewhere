# In this file we define the Flask application


import os

from flask import Flask
from .page_factory import PageFactory
from flask_bootstrap import Bootstrap
from .scrapp_launcher import Scrapper
from .fake_bdd import FakeBDD
from flask_pymongo import PyMongo



def create_app():
    """creates the app and makes routes"""
    app = Flask(__name__, static_url_path = "/static", static_folder = "static")
    Bootstrap(app)
    app.config['BOOTSTRAP_USE_CDN'] = True
    app.config['SECRET_KEY'] = 'thisisasecret'
    app.config['MONGO_URI'] = "mongodb://localhost:27017/ads"
    app.config['MONGO_DBNAME'] = 'ads'
    mongo = PyMongo(app)



    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass




    # The main page
    @app.route('/')
    @app.route('/index/')
    def main_page():
        page = PageFactory.generate_page('MAIN')
        return page.process()

    # The result page
    @app.route('/results', methods=('GET', 'POST'))
    def results_page():
        page = PageFactory.generate_page('RESULT')
        return page.process(mongo)

    @app.route('/error')
    def error_page():
        page = PageFactory.generate_page('ERROR')
        return page.process()

    @app.before_first_request
    def before_first_request():

        mongo.db.command('dropDatabase')

        # Launching the scrapping
        # scrapper = Scrapper(mongo)
        # scrapper.start()

        # For test only : create fake bdd
        FakeBDD.create_fake_bdd(mongo)


    return app
