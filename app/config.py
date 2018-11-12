import os


class Config(object):
    
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    DEBUG_TB_ENABLED = DEBUG
    SQLALCHEMY_RECORD_QUERIES = DEBUG
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    TEMPLATES_AUTO_RELOAD = True    

    SECRET_KEY = "bb2d178c-ae16-4be0-9926-764c552082e9"
    WTF_CSRF_SECRET_KEY = "99ef5388-12c3-4a10-9e98-a1a67b9d4d6a"

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://vzdnqoovnvgmgu:1582147d7b2ff4ee88b52ca47a48064cafb997fcea0d78bbac3cebf76fc7bbbe@ec2-54-217-235-159.eu-west-1.compute.amazonaws.com:5432/d8kstj8qf9g683'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CACHE_DEFAULT_TIMEOUT = 300  # seconds
    CACHE_TYPE = 'redis'
    # CACHE_REDIS_URL = os.environ.get('REDIS_URL') or \
        # 'redis://pratki-redis:6379'  # Use this for development
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://h:p4cf37f6f6b51abd95a99cd36aba622c6c370d922259e6a9e5a18143416b1ce6c@ec2-34-254-120-196.eu-west-1.compute.amazonaws.com:10589'

    RATELIMIT_STORAGE_URL = 'redis://h:p4cf37f6f6b51abd95a99cd36aba622c6c370d922259e6a9e5a18143416b1ce6c@ec2-34-254-120-196.eu-west-1.compute.amazonaws.com:10589'

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

    ALLOWED_EXTENSIONS = set(['txt'])
    UPLOAD_FOLDER = '/pratki-heroku/uploads'
