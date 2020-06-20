from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

class ImageInputForm(FlaskForm):
    image = FileField("Upload PNG or JPG Image", validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Upload Image")

class LargerImageForm(FlaskForm):
    image = FileField("Upload the Larger PNG or JPG Image", validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Create Image")