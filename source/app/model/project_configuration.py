import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)

app.secret_key = os.getenv("KEY")
app.config['SESSION_TYPE'] = 'filesystem'

session = Session(app)
login_manager = LoginManager(app)