from flask import current_app
from datetime import datetime

# Here can be defined template contexts


def footer_context():
    return {
        'now': datetime.utcnow(),
        'name': u'Krsteski'
    }


def cache_timeout_context():
    cache_timeout = current_app.config['CACHE_DEFAULT_TIMEOUT']
    return {
        'cache_timeout': cache_timeout
    }
