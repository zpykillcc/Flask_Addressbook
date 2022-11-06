from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    image_hash = db.Column(db.String(128))
    movies = db.relationship('Movie',backref='user')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    sex = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    qq = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # 外键


