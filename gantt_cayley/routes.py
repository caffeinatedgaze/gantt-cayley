from flask_login import login_user, current_user, logout_user, login_required
from flask import render_template, url_for, flash, redirect, request
from chart_builder import define_data, create_chart, delete_chart
from .forms import RegistrationForm, LoginForm
from gantt_cayley import app, bcrypt
from plotly.tools import get_embed
from re import compile
from db import driver

proj = [
    {
        'name': 'Gantt Cayley',
        'team': '17-7',
        'description': 'Shaun The Sheep',
        'chart_link': "https://plot.ly/~fenchelfen/32"
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
    return render_template('root.html', title='Feed')


def build_chart(project_id):
    project = driver.get_object_by_id('PROJECT', project_id)
    tasks = [driver.get_object_by_id('TASK', task_id)
             for task_id in project.task]
    df = define_data(tasks)
    project.chart_link = create_chart(df, title=project.name)
    return project


def build_charts():
    projects = [driver.get_object_by_id('PROJECT', x)
                for x in driver.get_object_by_id('GROUP', current_user.in_group[0]).project]
    for project in projects:
        tasks = [driver.get_object_by_id('TASK', task_id)
                 for task_id in project.task]
        df = define_data(tasks)
        print(df)
        project.chart_link = create_chart(df, title=project.name)
    return projects


@app.route('/home/')
@login_required
def home():
    projects = build_charts()
    print([x.name for x in projects])
    if current_user.in_group:
        return render_template('home.html', title='Home',
                               projects=projects,
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
        flash('Your account has been created! Try to login', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form, places=True)


@app.route('/view/<project_id>')
@login_required
def view_gantt(project_id):
    p = compile(r'height="[\d]*"')
    project = build_chart(project_id)
    if project:
        chart = p.sub('height=600', get_embed(project.chart_link))
        return render_template('view_gantt.html', title=project.name, chart=chart, places=False)
    else:
        flash("Failed to find '%s'" % project.name, 'danger')
        return redirect(url_for('home'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # print(len(driver.filter_by('USER')))
        # user = driver.get_quads(label='USER', relation='email', value=form.email.data)
        user = driver.filter_by(type='USER', email=form.email.data)
        # if user and bcrypt.check_password_hash(user[0].password, form.password.data):
        # yes, it's plaintext -- for the ease of using the generated dataset
        print(user, form.email.data, form.password.data)
        if user and user[0].password == form.password.data:
            login_user(user[0], remember=form.remember)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, places=True)


@app.route('/logout/')
def logout():
    # projects = [driver.get_object_by_id('PROJECT', x)
    #             for x in driver.get_object_by_id('GROUP', current_user.in_group[0]).project]
    projects = build_charts()
    for project in projects:
        delete_chart(project.chart_link)
    logout_user()
    return redirect(url_for('root'))
