import sqlite3

from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from forms import AdminUploadForm
admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [{'url': '.index', 'title': 'Admin panel'},
        {'url': '.listusers', 'title': 'List of users'},
        {'url': '.addStyle', 'title': 'Add style'},
        {'url': '.logout', 'title': 'Logout'}]

db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Admin-panel')


@admin.route('/login', methods=['POST', 'GET'])
def login():
    if isLogged():
        return redirect(url_for('.index'))

    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['psw'] == '12345':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Wrong login or password', 'error')
    return render_template('admin/login.html', title='Admin-panel')


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()
    return redirect(url_for('.login'))



@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))

    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f'SELECT email FROM users ORDER BY time DESC')
            list = cur.fetchall()
        except sqlite3.Error as e:
            print('Error' + str(e))

    return render_template('admin/listusers.html', title='List of users', menu=menu, list=list)

@admin.route('/add_style', methods=["POST", "GET"])
def addStyle():
    if not isLogged():
        return redirect(url_for('.login'))

    form = AdminUploadForm()
    if form.validate_on_submit():
        if db:
            try:
                cur = db.cursor()
                cur.execute(f'INSERT INTO styles(id, styleImage) VALUES(?, ?)', (form.admin_image_id.data, sqlite3.Binary(form.admin_image.data.read())))
                db.commit()
            except sqlite3.Error as e:
                print('Ошибка добавления стиля в БД ' + str(e))
    return render_template('admin/add_style.html', title='Admin adding style image', menu=menu, form=form)

