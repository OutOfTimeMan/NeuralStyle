import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from NDataBase import NDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm, UploadForm
from NeuralNetwork import *
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'enkjrgn3e45rt0342hf23kjfn2ekwlfn23wo4t'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6Lcah5IhAAAAAFC41-HyMhWMZvU4AdytE75LaqlW'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Lcah5IhAAAAAITJNj5FWcZWBbL2H8xMFoRiBYK2'
app.config['RECAPTCHA_DATA_ATTRS'] = {'theme': 'dark'}

menu = [{'name': 'NeuroStyle', 'url': '/'},
        {'name': 'Examples', 'url': '/examples'},
        {'name': 'About', 'url': '/about'}]

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access the editor'
login_manager.login_message_category = 'error1'


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


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


'''MAIL'''

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '6fhec6cz@gmail.com'
app.config['MAIL_PASSWORD'] = 'jsnpbdxevvpdwbot'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
s = URLSafeTimedSerializer('enkjrgn3e45rt0342hf23kjfn2ekwlfn23wo4t')

'''ROUTES'''


@app.route('/examples')
def examples():
    return render_template('examples.html', title='Examples', menu=menu)


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


@app.route('/confirm', methods=['GET', 'POST'])
@login_required
def confirm():
    if request.method == 'POST':
        email = current_user.getEmail()
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm Email', sender='6fhec6cz@gmail.com', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)
    return render_template('confirm.html', menu=menu, title='Email confirmation')


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        dbase.updateUserConfirmState(current_user.get_id())
    except SignatureExpired:
        return '<h1>The token has expired</h1>'
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html', title='About', menu=menu)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    form = UploadForm()
    if form.validate_on_submit():
        if form.image_origin.data:
            img = form.image_origin.data.read()
            stl = form.select.data
            dbase.updateUserImage(img, current_user.get_id())
            dbase.updateUserStyleImageId(stl, current_user.get_id())
            return redirect(url_for('result'))
    return render_template('index.html', menu=menu, form=form)


@app.route('/result')
@login_required
def result():
    return render_template('result.html', title='Result', menu=menu)


@app.route('/resultImage')
@login_required
def resultImage():
    imgNeuro = current_user.getImage()
    imgStyle = dbase.getStyleImageByID(current_user.getStyleID())['styleImage']
    imgRes = style(imgNeuro, imgStyle)
    h = make_response(imgRes)
    h.headers['ContentType'] = 'image/jpg'

    return h


@app.route('/getLoadingImage')
@login_required
def getLoadingImage():
    h = make_response(current_user.getImage())
    h.headers['ContentType'] = 'image/jpg'

    return h


if __name__ == '__main__':
    app.run(debug=True)
