from flask import render_template, Blueprint, request

main = Blueprint('main', __name__)

@main.route("/")
def index():

    return render_template("main.html")