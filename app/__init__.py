from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config


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

from app import routes, models
