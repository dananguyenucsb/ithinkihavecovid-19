from flask_wtf import FlaskForm
from wtforms import Form, TextField, validators, SubmitField
from wtforms.validators import DataRequired

# from flask_babel import lazy_gettext as _


class CreateEntryForm(FlaskForm):
    location = TextField("Location", validators=[DataRequired()])
    age = TextField("Age", validators=[DataRequired()])
    symptoms = TextField("Symptoms", validators=[DataRequired()])
    ip_address = TextField("IP Address", validators=[DataRequired()])
    travel_history = TextField(
        "Travel History", validators=[DataRequired()])
    submit = SubmitField('Sign In')
