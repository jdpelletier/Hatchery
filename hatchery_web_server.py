import os
import datetime

from Util import auto_file_write

from werkzeug.urls import url_parse
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required, UserMixin
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from home import home
from history import history
from forms import LoginForm

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

@app.route('/',methods=['POST', 'GET'])
##For testing
# @login_required
def home_():
    parent_directory = "/home/pi/Desktop/Hatchery/TestData"
    today = datetime.date.today()
    todaystr = today.isoformat()
    path = os.path.join(parent_directory, todaystr)
    filepath = os.path.join(str(path), "dataFile.txt")
    return home(filepath)

@app.route('/history',methods=['POST', 'GET'])
@login_required
def history_():
    parent_directory = "/home/pi/Desktop/Hatchery/TestData/"
    today = datetime.date.today()
    day = request.form.get("day", str(today.day))
    if len(day) == 1:
        day = "0" + day
    month = request.form.get("month", str(today.month))
    if len(month) == 1:
        month = "0" + month
    year = request.form.get("year", str(today.year))
    daystring = f"{year}-{month}-{day}"
    path = parent_directory + daystring
    filepath = os.path.join(str(path), "dataFile.txt")
    submit = request.form.get("submit")
    if submit:
        auto_file_write(filepath)
        return history(filepath, daystring, submit)
    return history(filepath, daystring, submit)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('home_'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home_')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=50009)
