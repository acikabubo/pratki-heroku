from app import db, lm
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    packages = db.relationship('Package', backref='user', lazy=True)


    def __repr__(self):
        """Repr."""
        return '<User {0}. {1}>'. format(self.id, self.nickname)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_no = db.Column(db.String(16), unique=True)
    shipped_on = db.Column(db.String(20))
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """Repr."""
        return '<Package {}>'.format(self.name)
