from flask import Response
from flask import Flask, render_template, redirect

from de.sphrilix.holy_greetings.dto.config import Config
from de.sphrilix.holy_greetings.web_app.forms.config_form import ConfigForm
from de.sphrilix.holy_greetings.web_app.forms.run_form import RunForm
from de.sphrilix.holy_greetings.web_app.service.bot_service import BotService

APP: Flask = Flask(__name__, template_folder="../../../../../templates/")
# APP: Quart = Quart(__name__, template_folder="../../../../../templates/")

APP.config['SECRET_KEY'] = 'you-will-never-guess'

BOT_SERVICE = BotService()


@APP.route("/")
def index() -> str:
    """
    Returns index page.
    :return: Index page.
    """
    run_form = RunForm()
    config_form = ConfigForm()
    c = BOT_SERVICE.get_config()
    return render_template("config.html",
                           running=BOT_SERVICE.is_running(),
                           run_form=run_form,
                           config_form=config_form,
                           config=c)


@APP.route("/start", methods=["POST"])
def start() -> Response:
    """
    Listen on start form.
    :return: Redirect to index.
    """
    form = RunForm()
    if form.validate_on_submit():
        BOT_SERVICE.token = form.token.data
        BOT_SERVICE.run()
    return redirect("/")


@APP.route("/config", methods=["POST"])
def config() -> Response:
    """
    Listen on config form
    :return: Redirect to index.
    """
    form = ConfigForm()
    if form.validate_on_submit():
        c = Config("", form.max_char.data, form.max_play.data, form.max_play_only.data, form.max_sound_greets.data,
                   form.max_size_sound_in_mb.data * 1000000)
        BOT_SERVICE.update_config(c)
    return redirect("/")
