import os


class Config(object):
    TEMPLATES_AUTO_RELOAD = True

    SECRET_KEY = "powerful secretkey"
    WTF_CSRF_SECRET_KEY = "a csrf secret key"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://vzdnqoovnvgmgu:1582147d7b2ff4ee88b52ca47a48064cafb997fcea0d78bbac3cebf76fc7bbbe@ec2-54-217-235-159.eu-west-1.compute.amazonaws.com:5432/d8kstj8qf9g683'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOWED_EXTENSIONS = set(['txt'])
    UPLOAD_FOLDER = '/pratki-heroku/uploads'

    # TODO: those settings should be env vars
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '1982853558673321',  # pratki facebook app
            'secret': 'ea3bb54866a4bc6667a78cabca0034be'  # pratki facebook app
        },
        'twitter': {
            'id': '3RzWQclolxWZIMq5LJqzRZPTl',
            'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
        }
    }
