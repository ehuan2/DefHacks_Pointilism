from flask import render_template, Blueprint, request, redirect, url_for
from flask_app.main.forms import ImageInputForm, LargerImageForm
from flask_app.main.utils import save_picture, generate_image
from PIL import Image
import os

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def index():

    image_form = ImageInputForm()
    larger_image_form = LargerImageForm()

    if image_form.validate_on_submit():
        if image_form.image.data:
            save_picture(image_form.image.data, output_size=(8, 8))

    images = [img_path for img_path in os.listdir("./flask_app/static/images")]

    return render_template("main.html", image_form=image_form, larger_image_form = larger_image_form, images = images)


@main.route("/generate_image", methods = ['POST'])
def generate_image_route():

    if request.method == 'POST':
        img = request.files.get("image")

        if img:
            larger_image = Image.open(request.files.get("image").stream)
            generate_image(larger_image=larger_image)

    return redirect(url_for('main.index'))