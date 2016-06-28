import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/db')
def db():
    return render_template('db.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/table/<name>')
def table(name):
    return render_template('table.html')

@app.route('/table/<name>/insert')
def insert(name):
    return render_template('insert.html')

@app.route('/table/<name>/delete')
def delete(name):
    return redirect(url_for('table', name=name))

if __name__ == '__main__':
    app.run()
