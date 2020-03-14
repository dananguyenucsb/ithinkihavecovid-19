from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    age = db.Column(db.Integer)
    symptoms = db.Column(db.String(255))
    ip_address = db.Column(db.String(32))
    travel_history = db.Column(db.String(255))

    def __init__(self, location, age, symptoms, ip_address, travel_history):
        self.location = location
        self.age = age
        self.symptoms = symptoms
        self.ip_address = ip_address
        self.travel_history = travel_history

    def __repr__(self):
        return "<Location %r>" % (self.location)


db.drop_all()
db.create_all()
users = User.query.all()
print([user.location for user in users])
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)


# db.drop_all()
# db.create_all()

# db.session.add(User(username="Flask", email="example@example.com"))
# db.session.commit()

# # print(User.query.filter_by(username='admin').first())
# users = User.query.all()
# print([user.email for user in users])
