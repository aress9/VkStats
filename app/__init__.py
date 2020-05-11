from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vkstats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.secret_key = '12345'
app.static_folder = 'static'

db = SQLAlchemy(app)
manager = LoginManager(app)

from app.models import User, Analytics


def checkAnalyticsDate():
    t = datetime.now()
    t2 = int(time.time()) - t.minute * 60 - t.second

    if not Analytics.query.filter_by(time=t2).first():
        db.session.add(Analytics(time=t2, requests=0))
        db.session.commit()


class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        data = [i[0] for i in db.session.query(Analytics.requests).all()]
        time = [i[0] * 1000 for i in db.session.query(Analytics.time).all()]
        return self.render('analytics_index.html', data=data, time=time)


admin = Admin(app, name='vkstats', template_mode='bootstrap3')
admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
admin.add_view(ModelView(User, db.session))

from app import routes

db.create_all()
