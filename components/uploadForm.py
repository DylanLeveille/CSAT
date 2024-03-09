"""Form for upload"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms.fields import *
from wtforms import SubmitField
from wtforms import validators


class UploadForm(FlaskForm):
    """Form that accepts the Excel input file."""

    validatorsFile = [
        FileRequired(message="No file selected"),
        FileAllowed(["xlsx"], message="File must be csv"),
    ]

    excel_file = FileField("", validators=validatorsFile)
    submit = SubmitField(label="Submit Control File", name="uploadControl")
