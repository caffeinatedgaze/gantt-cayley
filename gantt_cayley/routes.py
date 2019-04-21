from flask import render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm
from plotly.tools import get_embed
from re import compile
from gantt_cayley import app, bcrypt, login_manager
from db import driver

projects = [
    {
        'name': 'Gantt Cayley',
        'team': '17-7',
        'description': 'Shaun The Sheep',
        'chart_link': "https://plot.ly/~fenchelfen/0"
    },
    {
        'name': 'Cross Service',
        'team': '17-7',
        'description': 'Shalala',
        'chart_link': "https://plot.ly/~chris/1638"
    }
]


# @login_manager.user_loader
# def load_user(user_id):
#     return db.get_user(user_id)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html', title='Home', projects=projects, places=True)


@app.route('/about/')
def about():
    return render_template('about.html', title='About', places=True)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Create a new user instance
        # db.session.add(user)
        # db.session.commit()
        flash('You account has been created! Try to login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, places=True)


@app.route('/view/<project_name>')
def view_gantt(project_name):
    p = compile(r'height="[\d]*"')
    filtered_projects = list(filter(lambda x: x['name'] == project_name, projects))
    if filtered_projects:
        project = filtered_projects[0]
        chart = p.sub('height=600', get_embed(project['chart_link']))
        return render_template('view_gantt.html', title=project['name'], chart=chart, places=False)
    else:
        flash("Failed to find '%s'" % project_name, 'danger')
        return redirect(url_for('home'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gantt.com' and form.password.data == 'pass':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, places=True)
