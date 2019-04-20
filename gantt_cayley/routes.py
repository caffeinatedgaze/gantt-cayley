from flask import render_template, url_for, flash, redirect
from .forms import RegistrationForm, LoginForm
from plotly.tools import get_embed
from re import compile
from gantt_cayley import app

projects = [
    {
        'name': 'Gantt Cayley',
        'team': '17-7',
        'description': 'Shaun The Sheep',
        'chart_link': """
                        <a href="https://plot.ly/~fenchelfen/0/?share_key=v0hDkhbPYDbRwjQZPRJ5j5" target="_blank" title="gantt-simple-gantt-chart" style="display: block; text-align: center;">
                            <img src="https://plot.ly/~fenchelfen/0.png?share_key=v0hDkhbPYDbRwjQZPRJ5j5" alt="gantt-simple-gantt-chart"
                            style="max-width: 100%;"onerror="this.onerror=null;this.src='https://plot.ly/404.png';" />
                        </a>
                        <script data-plotly="fenchelfen:0" sharekey-plotly="v0hDkhbPYDbRwjQZPRJ5j5" src="https://plot.ly/embed.js" async></script>
                      """
    },
    {
        'name': 'Cross Service',
        'team': '17-7',
        'description': 'Shalala',
        'chart_link': """
                <a href="https://plot.ly/~fenchelfen/0/?share_key=v0hDkhbPYDbRwjQZPRJ5j5" target="_blank" title="gantt-simple-gantt-chart" style="display: block; text-align: center;">
                    <img src="https://plot.ly/~fenchelfen/0.png?share_key=v0hDkhbPYDbRwjQZPRJ5j5" alt="gantt-simple-gantt-chart"
                    style="max-width: 100%;"onerror="this.onerror=null;this.src='https://plot.ly/404.png';" />
                </a>
                <script data-plotly="fenchelfen:0" sharekey-plotly="v0hDkhbPYDbRwjQZPRJ5j5" src="https://plot.ly/embed.js" async></script>
              """
    }
]


@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html', title='Home', projects=projects, places=True)


@app.route('/about/')
def about():
    return render_template('about.html', title='About', places=True)


# @app.route('/register/', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash(f'Account created for {form.username.data}!', 'success')
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)

@app.route('/view/')
def view_gantt():
    p = compile(r'height="[\d]*"')
    chart = p.sub('height=600', get_embed("https://plot.ly/~fenchelfen/0"))
    return render_template('view_gantt.html', title='Gantt Chart', chart=chart, places=False)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gantt.com' and form.password.data == 'pass':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)
