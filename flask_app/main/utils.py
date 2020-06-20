from flask import current_app
from PIL import Image
import os
import secrets


def save_picture(form_picture, output_size):

    filename = form_picture.filename

    image_path = os.path.join(current_app.root_path, 'static/images', filename)

    img = Image.open(form_picture)

    img.thumbnail(output_size)

    img.save(image_path)

    return filename



def generate_image(larger_image):
    filename = secrets.token_hex(8)

    image_path = os.path.join(current_app.root_path, 'static/images', filename + ".png")

    img = Image.open(larger_image)

    img.save(image_path)

    return filename + ".png"