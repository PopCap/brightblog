from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# app is defined as an instance of class Flask in the __init__.py script
# making it a member of the app package
app = Flask(__name__)

# extensions need to be created and initialized right after the application instance
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# importing at bottom to get around circular imports
from app import routes, models