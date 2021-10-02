import os
import sqlite3
import uuid

from flask import Flask, request, redirect, url_for, flash, session, render_template


def get_db():
    return sqlite3.connect("db.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)


def setup():
    db = get_db()
    db.executescript(f"""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL
    );
    INSERT INTO users (username, password) VALUES ('admin', '{uuid.uuid4()}');
    """)


setup()

app = Flask(__name__)
app.secret_key = f'{uuid.uuid4().hex}'


# @app.route('/')
# def home():
#     redirect(url_for('index'))


@app.route('/', methods={'GET'})
def index():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    return 'No one:<br><br>Literally no one:<br><br>Hackerman: I\'m in'


@app.route('/login', methods={'GET', 'POST'})
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query_string = f'SELECT id FROM users WHERE username = \'{username}\' AND password = \'{password}\''
        user = get_db().execute(query_string).fetchone()
        if user is None:
            error = 'Invalid username and password'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)
    elif request.method == 'GET':
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
