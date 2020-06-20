from flask import current_app
from PIL import Image
import os

def save_picture(form_picture, output_size):
    
    image_path = os.path.join(current_app.root_path, 'static/images', form_picture.filename)
    
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(image_path)


def generate_image(larger_image):
    larger_image.show()
