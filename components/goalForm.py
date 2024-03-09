"""Form for attacker objectives (Attacker Profile)"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms.fields import *
from wtforms import SubmitField
from wtforms import validators
from wtforms import SelectMultipleField, widgets
from markupsafe import Markup

# class BootstrapListWidget(widgets.ListWidget):
 
#     def __call__(self, field, **kwargs):
#         kwargs.setdefault("id", field.id)
#         html = [f"<{self.html_tag} {widgets.html_params(**kwargs)}>"]
#         for subfield in field:
#             if self.prefix_label:
#                 html.append(f"<li class='list-group-item'>{subfield.label} {subfield(class_='form-check-input ms-1')}</li>")
#             else:
#                 html.append(f"<li class='list-group-item'>{subfield(class_='form-check-input me-1')} {subfield.label}</li>")
#         html.append("</%s>" % self.html_tag)
#         return Markup("".join(html))

# class MultiCheckboxField(SelectMultipleField):
#     """
#     A multiple-select, except displays a list of checkboxes.
 
#     Iterating the field will produce subfields, allowing custom rendering of
#     the enclosed checkbox fields.
#     """
#     widget = BootstrapListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

# class AssetForm(FlaskForm):
#     assetObjectives = MultiCheckboxField(label='Asset', #label will be overwritten by constructor (default is technically Asset)
#                                 choices=[('c', 'C'), 
#                                         ('i', 'I'), 
#                                         ('a', 'A') ]) #default setting for choices are C,I,A
    
#     def __init__(self, assetObjectives_label=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if assetObjectives_label != None:
#             self.assetObjectives.label = assetObjectives_label #put label as name of Asset

# class SubgoalForm(FlaskForm):
#     """Form with many asset objectives"""
#     subgoal = FieldList(FormField(AssetForm), min_entries=1)

class GoalForm(FlaskForm):
    """Form that accepts the dynamic attacker objectives and Budget."""
    budget = IntegerField(validators=[validators.NumberRange(min=0, max=None, message="Budget must be 0 or greater"),
                             validators.InputRequired()])

#     addresses = FieldList(FormField(SubgoalForm), min_entries=1)
# #add addr
# #remove addr
#     add = SubmitField("Add Address", name="addAddress")
#     remove = SubmitField("Remove Address", name="removeAddress")
#     submit = SubmitField(label="Find Optimal Control Strategies", name="findStrategies")

#     def validate(self, *args, **kwargs):      
#         print(self)                                           
#         if self.add.data or self.remove.data:
#             return True                                            

#         print (super().validate())
#         return super().validate()