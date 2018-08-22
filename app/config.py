import os


class Config(object):
    SECRET_KEY = "powerful secretkey"
    WTF_CSRF_SECRET_KEY = "a csrf secret key"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://vzdnqoovnvgmgu:1582147d7b2ff4ee88b52ca47a48064cafb997fcea0d78bbac3cebf76fc7bbbe@ec2-54-217-235-159.eu-west-1.compute.amazonaws.com:5432/d8kstj8qf9g683'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOWED_EXTENSIONS = set(['txt'])
    UPLOAD_FOLDER = '/pratki-heroku/uploads'
