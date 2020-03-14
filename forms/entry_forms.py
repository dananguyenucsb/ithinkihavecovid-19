from flask_wtf import FlaskForm
from wtforms import Form, TextField, validators, SubmitField
# from flask_babel import lazy_gettext as _


class CreateEntryForm(FlaskForm):
    location = TextField("Location", )
    age = TextField("Age", )
    symptoms = TextField("Symptoms", )
    ip_address = TextField("IP Address",)
    travel_history = TextField(
        "Travel History", )
    submit = SubmitField('Sign In')
