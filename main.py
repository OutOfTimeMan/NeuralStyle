import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response
from NDataBase import NDataBase
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'enkjrgn3e45rt0342hf23kjfn2ekwlfn23wo4t'


menu = [{'name': 'NeuroStyle', 'url': '/'},
        {'name': 'Examples', 'url': '/examples'},
        {'name': 'About', 'url': '/about'}]

'''DATABASE'''
DATABASE = '/tmp/neurostyle.db'
DEBUG = True

app.config.update(dict(DATABASE=os.path.join(app.root_path,'neurostyle.db')))

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
def index():
    return render_template('index.html', menu=menu)

@app.route('/examples')
def examples():
    return render_template('examples.html', menu=menu)

@app.route('/login')
def login():
    return render_template('login.html', menu=menu)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['name']) > 1 and len(request.form['email']) > 4 \
            and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.addUser(request.form['name'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
            flash("Неверно заполнены поля", "error")

    return render_template("register.html", menu=menu, title="Регистрация")

@app.route('/about')
def about():
    return render_template('about.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)