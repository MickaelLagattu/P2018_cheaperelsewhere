from flask_wtf import FlaskForm
from wtforms import StringField



class LinkForm(FlaskForm):
    """ Definition of the form in order to get the link """
    link = StringField(label="link")