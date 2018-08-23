from app import db, lm
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_no = db.Column(db.String(16), unique=True)
    shipped_on = db.Column(db.String(20))
    name = db.Column(db.String(64))

    def __repr__(self):
        """Repr."""
        return '<Package {}>'.format(self.name)
