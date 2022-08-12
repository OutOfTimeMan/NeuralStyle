from flask import Flask, render_template, request, g, flash, abort, redirect, url_for

app = Flask(__name__)

menu = [{'name': 'NeuroStyle', 'url': '/'},
        {'name': 'Examples', 'url': '/examples'},
        {'name': 'About', 'url': '/about'}]


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/examples')
def examples():
    return render_template('examples.html', menu=menu)

@app.route('/about')
def about():
    return render_template('about.html', menu=menu)

if __name__ == '__main__':
    app.run(debug=True)