from flask import Flask, render_template, request, Blueprint, redirect, flash, url_for
from flask_login import login_user, login_required
from app import app, db, vk
from app.models import User
from werkzeug.security import check_password_hash, generate_password_hash
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('stat.html')


@login_required
@app.route('/stat')
def stat():
    group = request.args.get('group')
    count = request.args.get('count')
    if 'vk.com' in group:
        group = group[group.index('/')]
    group_name, group_image = vk.get_profile_info(group)
    average, data = vk.get_all_statistic(group, int(count))
    map_data = vk.get_countries(group)
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
            return redirect(url_for('login_page'))
    else:
        flash('Заполните поля для регистрации')
    return render_template('register.html')