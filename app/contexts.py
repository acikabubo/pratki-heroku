from datetime import datetime

# Here can be defined template contexts

def footer_context():
    return {
    	'now': datetime.utcnow(),
    	'name': u'Krsteski'
    }
    