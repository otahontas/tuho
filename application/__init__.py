from flask import Flask
app = Flask(__name__)

# database
from flask_sqlalchemy import SQLAlchemy


import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookmarks.db"
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# application
from application import views

# create tables if they don't exist
try:
    db.create_all()
except:
    pass