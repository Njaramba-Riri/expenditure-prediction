import logging 
import click
from webapp import db
from .auth.models import User

log = logging.getLogger(__name__)

def register(app):
    """Creates click commands for the apllication.

    Args:
        app (Any): An instance of flask app.
    """
    @app.cli.command('create-user')
    @click.argument('username')
    @click.argument('password')
    def create_user(username, password):
        user = User()
        user.username = username
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            click.echo("User {0} added ".format(username))
        except Exception as e:
            log.error("Failed to add user: %s Error: %s" % (username, e))
            db.session.rollback()

    @app.cli.command('list-routes')
    def list_routes():
        for url in app.url_map.iter_rules():
            click.echo("%s %s %s" % (url.rule, url.methods, url.endpoint))


    
