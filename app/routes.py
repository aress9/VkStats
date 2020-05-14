from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, checkAnalyticsDate
from app.vk import Vk
from app.models import User, Analytics
from werkzeug.security import check_password_hash, generate_password_hash
from requests import get
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/stat')
@login_required
def stat():
    vk = Vk(current_user.vk_token)
    group = request.args.get('group')
    count = request.args.get('count')
    if 'vk.com' in group:
        group = group[group.index('/')]
    group_name, group_image = vk.get_profile_info(group)
    average, data = vk.get_all_statistic(group, int(count))
    map_data = vk.get_countries(group)

    checkAnalyticsDate()
    analyt = Analytics.query.first()
    analyt.requests += 1
    db.session.commit()

    return render_template('stat.html', likes=average[0],
                           comments=average[1],
                           reposts=average[2],
                           views=average[3],
                           group=group,
                           group_name=group_name,
                           group_image=group_image,
                           likes_data=data['likes'],
                           comments_data=data['comments'],
                           reposts_data=data['reposts'],
                           views_data=data['views'],
                           time_data=data['dates'],
                           labels=data['labels'],
                           map_data=map_data
                           )


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        print(login, password)
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)

            return redirect(url_for('index'))
        else:
            flash('Логин или пароль введены не корректно')
    else:
        flash('Заполните поля для входа')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        print(login, password, password2)
        if not (login and password and password2):
            flash('Заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            pass_hash = generate_password_hash(password)
            new_user = User(login=login, password=pass_hash)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for(f'register_vk'))
    else:
        flash('Заполните поля для регистрации')
    return render_template('register.html')


@app.route('/register_vk', methods=['GET', 'POST'])
def register_vk():
    if request.args.get('code'):
        data = get(
            f'https://oauth.vk.com/access_token?client_id=7457856&client_secret=tr4P7JWfpNzgL00F34jE&redirect_uri=http://b9ade7a0.ngrok.io/register_vk&code={request.args.get("code")}').content
        print(data)
        user = User.query.filter_by(login=current_user.login).first()
        user.vk_token = json.loads(data)['access_token']
        db.session.commit()
        return redirect('index')

    return render_template('register_vk.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('index')
