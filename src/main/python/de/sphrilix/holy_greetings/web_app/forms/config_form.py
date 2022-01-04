from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField

from de.sphrilix.holy_greetings.persistence.config_handler import ConfigHandler


class ConfigForm(FlaskForm):
    """c = ConfigHandler().read()
    max_char = StringField("max_char", default=c.max_char)
    max_play = IntegerField("max_play", default=c.max_play)
    max_play_only = IntegerField("max_play_only", default=c.max_play_only)"""
    max_char = IntegerField("max_char")
    max_play = IntegerField("max_play")
    max_play_only = IntegerField("max_play_only")
    submit = SubmitField("Submit")
