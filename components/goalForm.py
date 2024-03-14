"""Form for attacker objectives (Attacker Profile)"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms.fields import *
from wtforms import SubmitField
from wtforms import validators
from wtforms import SelectMultipleField, widgets
from markupsafe import Markup


class GoalForm(FlaskForm):
    """Form that accepts the dynamic attacker objectives and Budget."""
    budget = IntegerField(validators=[validators.NumberRange(min=0, max=None, message="Budget must be 0 or greater"),
                             validators.InputRequired()])
