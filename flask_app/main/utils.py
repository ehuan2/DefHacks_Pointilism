from flask import current_app
from PIL import Image
from image_processing.main import get_processed_image
import os
import secrets


# the following adds the image as a byte format, and reformats it
def save_picture(form_picture, output_size):

    filename = secrets.token_hex(8)

    img = Image.open(form_picture)

    img = img.resize(output_size)

    return (filename, img)

# generates the larger image
def generate_image(larger_image, smaller_images, output_size):

    larger_image = Image.open(larger_image)

    larger_image = larger_image.resize(output_size)

    img = get_processed_image(larger_image, smaller_images)

    return [create_bytes_image(larger_image), create_bytes_image(img)]

# creates the byte versions available in html
def create_bytes_image(image):
     # next is base 64 encoding it for both images
    import base64
    from io import BytesIO

    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    encoded = base64.b64encode(buffered.getvalue())

    encoded = encoded.decode("utf-8")

    mime = "image/jpeg"
    uri = "data:%s;base64, %s" % (mime, encoded)
    return uri