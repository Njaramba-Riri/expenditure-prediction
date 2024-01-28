from flask import Blueprint, redirect, url_for, session

babel_blueprint = Blueprint('babel', __name__, url_prefix="/letsgo")

@babel_blueprint.route('/<string:locale>')
def index(locale):
    session[locale] = locale
    return redirect(url_for('app.index'))