from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from .forms import RegistrationForm, LoginForm
from gantt_cayley import app, bcrypt
from plotly.tools import get_embed
from re import compile
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


@app.route('/')
def root():
    return render_template('root.html', title='home')


@app.route('/home/')
@login_required
def home():
    print(current_user.in_group)
    if current_user.in_group:
        return render_template('home.html', title='Home',
                               projects=driver.get_object_by_id(object_type='GROUP', object_id=current_user.in_group[0]),
                               places=True)
    else:
        return redirect(url_for('about'))


@app.route('/about/')
def about():
    return render_template('about.html', title='About', places=True)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
@login_required
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = driver.get_quads(label='USER', relation='email', value=form.email.data)
        if user and bcrypt.check_password_hash(user[0].password, form.password.data):
            login_user(user[0], remember=form.remember)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, places=True)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('root'))
