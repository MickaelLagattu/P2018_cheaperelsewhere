# In this file we define the Flask application


import os

from flask import Flask
from .database import Database
from .page_factory import PageFactory
from flask_bootstrap import Bootstrap



def create_app():
    """creates the app and makes routes"""
    app = Flask(__name__, instance_relative_config=True, static_url_path = "/static", static_folder = "static")
    Bootstrap(app)
    app.config['BOOTSTRAP_USE_CDN'] = True
    app.config['SECRET_KEY'] = 'thisisasecret'


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Enabling the database interactions
    database = Database(app)




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
        return page.process(database)

    @app.route('/error')
    def error_page():
        page = PageFactory.generate_page('ERROR')
        return page.process()

    #Here we can launch the scrapper



    return app
