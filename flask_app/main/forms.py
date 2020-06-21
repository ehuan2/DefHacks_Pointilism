from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

class ImageInputForm(FlaskForm):
    image = FileField("Upload JPG Image", validators = [FileAllowed(['jpg'])])
    submit = SubmitField("Upload Image")

class LargerImageForm(FlaskForm):
    image = FileField("Upload the Larger JPG Image", validators = [FileAllowed(['jpg'])])
    submit = SubmitField("Create Image")