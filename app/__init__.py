from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# app is defined as an instance of class Flask in the __init__.py script
# making it a member of the app package
app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# importing at bottom to get around circular imports
from app import routes, models