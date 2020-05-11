from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
from app.vk import Vk

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vkstats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '12345'
app.static_folder = 'static'
db = SQLAlchemy(app)
manager = LoginManager(app)

with open('secret.json', 'r') as file:
    secret = json.loads(file.read())
    vk = Vk(secret['login'], secret['password'])

from app import routes

db.create_all()
