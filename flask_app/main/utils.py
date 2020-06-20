from flask import current_app
from PIL import Image
import os

def save_picture(form_picture):
    
    image_path = os.path.join(current_app.root_path, 'static/images', form_picture.filename)

    output_size = (8, 8)
    
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(image_path)

    img.show()