from datetime import datetime
import app

# Here can be defined template contexts


def footer_context():
    return {
        'now': datetime.utcnow(),
        'name': u'Krsteski'
    }


def cache_timeout_context():
    return {
        'cache_timeout': 10
    }
