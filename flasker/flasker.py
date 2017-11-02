# all the imports
import os
import sqlite3
from pprint import pprint
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flasker.db'),
    SECRET_KEY='dev_key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('FLASKER_SETTINGS', silent=True)

if app.config['DEBUG']:
    config_dict = app.config
    for k, v in config_dict.items():
        print(k, v)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        if error:
            print('Got error on teardown: {}'.format(error))
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute(
        'select title, text from entries order by id desc'
    )
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)