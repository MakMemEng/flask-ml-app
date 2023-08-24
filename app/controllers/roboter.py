from flask import Flask, redirect, render_template, request, url_for

import settings

app = Flask(__name__, template_folder="../../templates/", static_folder="../../static/")


class WebServer(object):
    def start(self, debug=False):
        app.run(host="0.0.0.0", port=settings.PORT, debug=debug)


server = WebServer()

ROBOT_NAME = "Roboko"


@app.route("/", methods=["GET", "POST"])
def hello() -> str:
    if request.method == "POST":
        user_name = request.form.get("user_name").strip()
        return render_template("evaluate_restaurant.html", user_name=user_name)
    return render_template("hello.html", name=ROBOT_NAME)


@app.route("/restaurant/rate", methods=["GET", "POST"])
def restaurant_rate() -> str:
    if request.method == "POST":
        user_name = request.form.get("user_name").strip()
        rate = request.form.get("rate").strip()
        restaurant = request.form.get("restaurant").strip()
        return render_template("good_by.html", user_name=user_name)
