from flask import Response
from flask import Flask, render_template, redirect

from de.sphrilix.holy_greetings.web_app.forms.config_form import ConfigForm
from de.sphrilix.holy_greetings.web_app.forms.run_form import RunForm
from de.sphrilix.holy_greetings.web_app.service.bot_service import BotService

APP: Flask = Flask(__name__, template_folder="../../../../../templates/")

APP.config['SECRET_KEY'] = 'you-will-never-guess'

BOT_SERVICE = BotService()


@APP.route("/")
def index() -> str:
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
    form = RunForm()
    if form.validate_on_submit():
        BOT_SERVICE.token = form.token.data
        BOT_SERVICE.run()
    return redirect("/")


@APP.route("/config", methods=["POST"])
def config() -> Response:
    form = ConfigForm()
    if form.validate_on_submit():
        print("exe")
        BOT_SERVICE.update_config(form.max_char.data, form.max_play.data, form.max_play_only.data)
    return redirect("/")
