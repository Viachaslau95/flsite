from werkzeug.security import generate_password_hash, check_password_hash

from mysite import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=True)
    psw = db.Column(db.String(500), nullable=False)
    profiles = db.relationship('Profile', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.psw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.psw, password)

    def __repr__(self):
        return f"<Users id: {self.id}, name: {self.username}> "


class Profile(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(500))
    email = db.Column(db.String(300))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User', backref=db.backref('profiles', lazy=True))

    def __init__(self, name, old, city, email, user):
        self.name = name
        self.old = old
        self.city = city
        self.email = email
        self.user = user

    def __repr__(self):
        return f"Profile: {self.id}"


