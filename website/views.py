from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home", methods=["GET"])
def home():
    return render_template("index.html")

@views.route("/services")
def services():
    return render_template("services.html")

@views.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")