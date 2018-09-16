import flask
from flask import Blueprint, redirect, url_for
from flask_principal import PermissionDenied

bp_site = Blueprint('site', __name__, url_prefix='/')


@bp_site.route('/', methods=['GET'])
def home():
    return flask.render_template('/login/base.html')


@bp_site.route('/dashboard', methods=['GET'])
def dashboard():
    return flask.render_template('home.html')


@bp_site.route('/forbidden', methods=['GET'])
def forbidden():
    return flask.render_template('site/forbidden.html'), 403


def internal_server_error(exception):
    if isinstance(exception, PermissionDenied):
        return redirect(url_for('common.forbidden'))
    return flask.render_template('site/internal_server_error.html'), 500


def not_found(exception):
    return flask.render_template('site/not_found.html'), 404
