from flask import url_for, request, flash, session, redirect, render_template
from flask_login import current_user, LoginManager

from mysite import app, db
from mysite.models import User, Profile

menu = [
    {"name": "Установка", "url": "install-flask"},
    {"name": "Первое приложение", "url": "first-app"},
    {"name": "Обратная связь", "url": "contact"},
]

login_manager = LoginManager(app)

@app.route("/")
def index():
    print(url_for('index'))
    return render_template('index.html', menu=menu)


@app.route("/about")
def about():
    print(url_for('about'))
    return render_template('about.html', title="О сайте", menu=menu)


@app.route("/register", methods=("POST", "GET"))
def register():

    if request.method == "POST":
        username = request.form['username']
        psw = request.form['psw']
        u = User(username, psw)
        db.session.add(u)
        db.session.commit()

        return redirect(url_for('profile'))
    return render_template("/register.html", title="Регистрация", menu=menu)


@app.route("/profile", methods=("POST", "GET"))
def profile():
    if request.method == "POST":
        name = request.form['name']
        old = request.form['old']
        city = request.form['city']
        email = request.form['email']
        u_id = current_user.id
        prof = Profile(name, old, city, email, user=u_id)
        db.session.add(prof)
        db.session.commit()

    return render_template("/profile.html", title="Сохранить", menu=menu)


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
