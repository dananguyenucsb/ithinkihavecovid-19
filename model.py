from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.dialects.postgresql import ARRAY


app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LfkN-EUAAAAAMEUxpQGg7DdGHqhz0eY0_2S5aKu'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LfkN-EUAAAAADXeLuqzoBOAg0F3f-b_oQEPiSzL'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    age = db.Column(db.Integer)
    symptoms = db.Column(db.String(), default=[])
    ip_address = db.Column(db.String(255))
    tested = db.Column(db.String(255))
    in_contact = db.Column(db.String(255))

    def __init__(self, city, state, age, symptoms, ip_address, tested, in_contact):
        self.city = city
        self.state = state
        self.age = age
        self.symptoms = symptoms
        self.ip_address = ip_address
        self.tested = tested
        self.in_contact = in_contact

    def __repr__(self):
        return "<Location %r>" % (self.location)


# db.drop_all()
db.create_all()
