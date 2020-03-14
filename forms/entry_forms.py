from flask_wtf import FlaskForm, RecaptchaField
from wtforms import Form, TextField, validators, SubmitField, SelectField, StringField, SelectMultipleField
from wtforms.validators import DataRequired
# https://pusher.com/tutorials/google-recaptcha-flask
# from flask_babel import lazy_gettext as _


class CreateEntryForm(FlaskForm):
    city = TextField("City", validators=[DataRequired()])
    state = TextField("State", validators=[DataRequired()])
    age = TextField("Age", validators=[DataRequired()])
    symptoms = SelectMultipleField("Symptoms", choices=[('Fatigue', 'Fatigue'), ('Dry Cough', 'Dry Cough'), ('Fever', 'Fever'), (
        'Shortness of Breath', 'Shortness of Breath')], validators=[DataRequired()])
    ip_address = TextField("IP Address", validators=[DataRequired()])

    tested = SelectField(
        "Tested", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    recaptcha = RecaptchaField()


class CoronaSearchForm(FlaskForm):
    choices = [('City', 'City'),
               ('State', 'State'),
               ('Age', 'Age')]
    select = SelectField('Search:', choices=choices)
    search = StringField('')
