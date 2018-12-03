# In this file we define the Flask application

from flask import Flask

import os

from flask import Flask, render_template, request


def create_app():
    """creates the app and makes routes"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')  # Default database path
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Enabling the database interactions
    from . import db
    db.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # The main page
    @app.route('/')
    @app.route('/index/')
    def main_page():
        return render_template("main_page.html")

    # The result page
    @app.route('/results', methods=('GET', 'POST'))
    def results_page():
        if request.method == 'POST':
            link = request.form['link']

            # Send the link to another part of the program for processing

        return render_template("results.html")

    return app
