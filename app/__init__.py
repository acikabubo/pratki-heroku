from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_assets import Environment
from .config import Config
from .assets import bundles


# Initialize flask app
app = Flask(__name__)
app.config.from_object(Config)

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

from app import routes, models
