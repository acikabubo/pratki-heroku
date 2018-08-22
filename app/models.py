from app import db


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_no = db.Column(db.String(16), unique=True)
    shipped_on = db.Column(db.String(20))
    name = db.Column(db.String(64))

    def __repr__(self):
        """Repr."""
        return '<Package {}>'.format(self.name)
