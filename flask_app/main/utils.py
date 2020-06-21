from flask import current_app
from PIL import Image
from image_processing.main import get_processed_image
import os
import secrets


# the following adds the images to the 8images file, and then returns the path to it
def save_picture(form_picture, output_size):

    filename = secrets.token_hex(8)

    image_path = f'./image_processing/8images/{filename}'

    img = Image.open(form_picture)

    img.resize(output_size)

    img.save(image_path)

    return filename

def generate_image(larger_image):
    filename = secrets.token_hex(8)

    def create_path(index):
        return os.path.join(current_app.root_path, 'static/images', filename + f"{index}.png")

    image_path = create_path(0)

    img = Image.open(larger_image)

    img.save(image_path)

    img = get_processed_image(img)

    img.save(create_path(1))

    return [filename + "0.png", filename + "1.png"]