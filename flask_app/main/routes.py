from flask import render_template, Blueprint, request, redirect, url_for, make_response
from flask_app.main.forms import ImageInputForm, LargerImageForm
from flask_app.main.utils import save_picture, generate_image
from PIL import Image
import os
import secrets

cookies_dict = {}
larger_cookies_dict = {}

main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
def index():

    # the cookies stuff!
    cookie = request.cookies.get('userID')

    # creates a cookie if it doesn't exist
    if not cookie:
        cookie = secrets.token_hex(8)
        cookies_dict[cookie] = {}

    if not cookies_dict.get(cookie):
        cookies_dict[cookie] = {}

    if not larger_cookies_dict.get(cookie):
        larger_cookies_dict[cookie] = []

    # the different forms, smaller image and larger
    image_form = ImageInputForm()
    larger_image_form = LargerImageForm()

    if image_form.validate_on_submit():

        if image_form.image.data:
        
            filename, picture = save_picture(
                image_form.image.data, output_size=(8, 8))

            # adds in an image based on the cookie
            cookies_dict[cookie][filename] = picture


    # gets the images
    images = larger_cookies_dict.get(cookie)

    # prepares a response
    resp = make_response(render_template("main.html", image_form=image_form,
                                         larger_image_form=larger_image_form, images=images))

    resp.set_cookie('userID', cookie)
    return resp


@main.route("/generate_image", methods=['POST'])
def generate_image_route():

    if request.method == 'POST':
        img = request.files.get("image")

        if img:
            larger_image = request.files.get("image").stream

            cookie = request.cookies.get('userID')

            # creates a cookie if it doesn't exist
            if not cookie:
                cookie = secrets.token_hex(8)

            # creates the cookies
            if not cookies_dict.get(cookie):
                cookies_dict[cookie] = {}

            if not larger_cookies_dict.get(cookie):
                larger_cookies_dict[cookie] = []
                
            larger_cookies_dict[cookie].extend(generate_image(larger_image, cookies_dict.get(cookie), (256,256)))

    return redirect(url_for('main.index'))