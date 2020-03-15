from flask_wtf import FlaskForm, RecaptchaField
from wtforms import Form, widgets, TextField, validators, SubmitField, SelectField, StringField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
# https://pusher.com/tutorials/google-recaptcha-flask
# from flask_babel import lazy_gettext as _


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def my_length_check(form, field):
    if len(field.data) > 2:
        raise ValidationError('Field must be 2 characters')


class CreateEntryForm(FlaskForm):
    city = TextField("City", validators=[DataRequired()])
    state = TextField("State", validators=[
                      DataRequired(), my_length_check])
    age = IntegerField("Age", validators=[
        NumberRange(min=0, max=99)])
    symptoms = MultiCheckboxField("Symptoms", choices=[('Fatigue', 'Fatigue'), ('Dry Cough', 'Dry Cough'), ('Fever', 'Fever'), (
        'Shortness of Breath', 'Shortness of Breath')], validators=[DataRequired()])
    ip_address = TextField("IP Address", validators=[DataRequired()])

    tested = SelectField(
        "Tested", choices=[('Waiting', 'Waiting'), ('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    in_contact = SelectField(
        "In Contact", choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    coordinates = TextField("Coordinates", validators=[DataRequired()])
    submit = SubmitField('Submit')
    # recaptcha = RecaptchaField()


class CoronaSearchForm(FlaskForm):
    choices = [('City', 'City'),
               ('State', 'State'),
               ('Age', 'Age')]
    select = SelectField('Search:', choices=choices)
    search = StringField('')
