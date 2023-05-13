from functools import wraps
import click
from decouple import config
from flask import Flask, redirect, url_for, g, jsonify
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager(app)

app.secret_key = config('SECRET_KEY', cast=str)

from potatopy.database import db_session, init_db

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.user.role not in roles:
                return jsonify({'message':'Acesso negado.', 'usuario': g.user.login}), 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@click.command("init-db")
def init_db_command():
    init_db()
    click.echo('Database created !')

app.cli.add_command(init_db_command)

from potatopy import auth

app.register_blueprint(auth.auth)
