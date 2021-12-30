from flask import Flask, render_template

app: Flask = Flask(__name__, template_folder="../templates/")


@app.route('/')
def config_html():
    return render_template("config.html")


print(app.template_folder)
app.run()
