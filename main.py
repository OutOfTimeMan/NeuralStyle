import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from NDataBase import NDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm



app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'enkjrgn3e45rt0342hf23kjfn2ekwlfn23wo4t'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the editor'
login_manager.login_message_category = 'error1'

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


menu = [{'name': 'NeuroStyle', 'url': '/'},
        {'name': 'Examples', 'url': '/examples'},
        {'name': 'About', 'url': '/about'}]

'''DATABASE'''
DATABASE = '/tmp/neurostyle.db'
DEBUG = True
MAX_CONTENT_LENGTH = 4 * 1024 * 1024

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'neurostyle.db')))


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = NDataBase(db)


'''ROUTES'''


@app.route('/')
@login_required
def index():
    return render_template('index.html', menu=menu)


@app.route('/examples')
def examples():
    return render_template('examples.html', title='Examples', menu=menu)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.getUserByEmail(form.email.data)
        if user and check_password_hash(user['psw'], form.psw.data):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(url_for('index'))

        flash('Неверный логин или пароль', "error")
    return render_template('login.html', menu=menu, form=form)





@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        res = dbase.addUser(form.email.data, hash)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    return render_template("register.html", menu=menu, title="Registration", form=form)


@app.route('/about')
def about():
    return render_template('about.html', title='About', menu=menu)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = dbase.updateUserImage(img, current_user.get_id())
                if not res:
                    flash("File must be .jpg or .jpeg", "error")
                    return redirect(url_for('index'))
                flash('Successful', 'success')
            except FileNotFoundError as e:
                flash('File error reading', 'error')

        else:
            flash('Image not added. Error.', 'error')

    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('about.html', title='Result', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)
