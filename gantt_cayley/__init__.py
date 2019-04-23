from flask import Flask
from .forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from chart_builder import delete_chart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e55ce9012c843e5d1d84494a5cfac678'
app.jinja_env.globals.update(clever_function=delete_chart)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from gantt_cayley import routes