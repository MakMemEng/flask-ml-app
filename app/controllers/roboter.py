from flask import Flask, redirect, render_template, request, url_for

import settings

app = Flask(__name__, template_folder="../../templates/")


class WebServer(object):
    def start(self, debug=False):
        app.run(host="0.0.0.0", port=settings.PORT, debug=debug)


server = WebServer()

ROBOT_NAME = "Roboko"


@app.route("/", methods=["GET", "POST"])
def hello() -> str:
    return render_template("hello.html", name=ROBOT_NAME)
