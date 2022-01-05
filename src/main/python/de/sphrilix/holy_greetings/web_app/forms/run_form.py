from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RunForm(FlaskForm):
    """
    Back end representation of the run form called on start.
    """

    token = StringField("Token")
    submit = SubmitField("Start")


