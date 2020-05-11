from app import db, manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    vk_token = db.Column(db.String(255), unique=True)


class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, unique=True, nullable=False)
    requests = db.Column(db.Integer)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
