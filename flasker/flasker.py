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
