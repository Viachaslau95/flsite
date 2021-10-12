import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, url_for, request, flash, session, redirect, abort, g, render_template
from flask_sqlalchemy import SQLAlchemy

from models import app, db, Users

menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]


@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        username = request.form['username']
        psw = request.form['psw']

        db.session.add(Users(username, psw))
        db.session.commit()

        # name = request.form['name']
        # old = request.form['old']
        # city = request.form['city']
        #
        # db.session.add(Profiles(name, old, city))
        # db.session.commit()
        # except:
        #     db.session.rollback()
        #     print("Ошибка добавления в БД")
        return redirect("/profiles.html")
    return render_template("/register.html", title="Регистрация", menu=menu)


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title="О сайте", menu=menu)


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Пользователь: {username}"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title="Обратная связь", menu=menu)


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "Test Flask" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация', menu=menu)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена", menu=menu), 404


if __name__ == "__main__":
    app.run(debug=True)
