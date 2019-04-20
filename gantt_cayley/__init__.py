from flask import Flask
from .forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e55ce9012c843e5d1d84494a5cfac678'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

from gantt_cayley import routes
