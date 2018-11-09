from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_assets import Environment
from flask_sslify import SSLify
from flask_caching import Cache

from .config import Config
from .assets import bundles
from .contexts import *

# Initialize flask app
app = Flask(__name__)
app.config.from_object(Config)

# Define template contexts
app.context_processor(footer_context)
app.context_processor(cache_timeout_context)

# Initialize cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

# Redirects from http to https
SSLify(app)

# Initialize bootstrap
Bootstrap(app)

# Initialize login manager
lm = LoginManager(app)
lm.login_view = 'index'

# Initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize assets
assets = Environment(app)
assets.register(bundles)

from .views import *
