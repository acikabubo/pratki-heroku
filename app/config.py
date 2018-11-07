import os


class Config(object):
    TEMPLATES_AUTO_RELOAD = True

    SECRET_KEY = "bb2d178c-ae16-4be0-9926-764c552082e9"
    WTF_CSRF_SECRET_KEY = "99ef5388-12c3-4a10-9e98-a1a67b9d4d6a"

    CACHE_DEFAULT_TIMEOUT = 60

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://vzdnqoovnvgmgu:1582147d7b2ff4ee88b52ca47a48064cafb997fcea0d78bbac3cebf76fc7bbbe@ec2-54-217-235-159.eu-west-1.compute.amazonaws.com:5432/d8kstj8qf9g683'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ALLOWED_EXTENSIONS = set(['txt'])
    UPLOAD_FOLDER = '/pratki-heroku/uploads'

    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': os.environ.get('FB_ID'),         # pratki facebook app
            'secret': os.environ.get('FB_SECRET')  # pratki facebook app
        },
        'google': {
            'id': os.environ.get('G_ID'),         # pratki google app
            'secret': os.environ.get('G_SECRET')  # pratki google app
        }
    }
