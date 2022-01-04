from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField


class ConfigForm(FlaskForm):
    max_char = IntegerField("max_char")
    max_play = IntegerField("max_play")
    max_play_only = IntegerField("max_play_only")
    max_sound_greets = IntegerField("max_sound_greets")
    max_size_sound_in_mb = IntegerField("max_size_sound_in_mb")
    submit = SubmitField("Submit")
