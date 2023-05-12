
import click
from flask import Flask
from decouple import config

app = Flask(__name__)

app.secret_key = config['SECRET_KEY']

from potatopy.database import db_session, init_db
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
