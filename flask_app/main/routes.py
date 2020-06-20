from flask import render_template, Blueprint, request
from flask_app.main.forms import ImageInputForm
from flask_app.main.utils import save_picture

main = Blueprint('main', __name__)

@main.route("/", methods = ['GET', 'POST'])
def index():

    image_form = ImageInputForm()

    if image_form.validate_on_submit():
        if image_form.image.data:
            save_picture(image_form.image.data)
        else:
            print("No image given!")

    return render_template("main.html", image_form = image_form)