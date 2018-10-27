from app import db, lm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class ExternalLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False, default='')
    ext_logins = db.relationship('ExternalLogin', backref='user', lazy=True)
    packages = db.relationship('Package', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Repr."""
        return '<User {0}. {1}>'. format(self.id, self.nickname)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_no = db.Column(db.String(16), unique=True)
    shipped_on = db.Column(db.Date)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """Repr."""
        return '<Package {}>'.format(self.name)
