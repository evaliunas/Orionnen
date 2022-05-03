from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orionnen.db'
app.config['SECRET_KEY'] = 'DedsDfp7QZXfJaIoOZo3OEO3cgrhyJbt'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.hostinger.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'e.valiunas@.com'
app.config['MAIL_PASSWORD'] = '093328bolton'
mail = Mail(app)

from orionnen import routes