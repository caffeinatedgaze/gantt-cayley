from flask import Flask
from .forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e55ce9012c843e5d1d84494a5cfac678'

from gantt_cayley import routes
