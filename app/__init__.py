from flask import Flask
# from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


import os
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://vzdnqoovnvgmgu:1582147d7b2ff4ee88b52ca47a48064cafb997fcea0d78bbac3cebf76fc7bbbe@ec2-54-217-235-159.eu-west-1.compute.amazonaws.com:5432/d8kstj8qf9g683'
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Initialize flask app
app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
