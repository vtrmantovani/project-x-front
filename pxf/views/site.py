from datetime import datetime

import flask
from flask import Blueprint
from flask import current_app as app
from flask import redirect, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_principal import (AnonymousIdentity, Identity, PermissionDenied,
                             UserNeed, identity_changed, identity_loaded)

from pxf import db
from pxf.forms import LoginForm
from pxf.models import User

bp_site = Blueprint('site', __name__, url_prefix='/')


@bp_site.route('/', methods=['GET'])
@login_required
def home():
    return flask.render_template('home.html')


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user
    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))


@bp_site.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flask.flash('Credenciais inválidas', 'error')
        if user and not user.enabled:
            flask.flash('Usuario inativo', 'error')
        if user and user.check_password(password):

            user.last_login_dt = datetime.utcnow()
            db.session.commit()

            login_user(user)

            # Tell Flask-Principal the identity changed
            identity_changed.send(app._get_current_object(),
                                  identity=Identity(user.id))

            next_action = flask.request.args.get('next')
            return flask.redirect(next_action or flask.url_for('site.home'))

    return flask.render_template('login/login.html', form=form)


@bp_site.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(app._get_current_object(),
                          identity=AnonymousIdentity())

    return flask.redirect(flask.url_for('site.login'))


@bp_site.route('/forbidden', methods=['GET'])
def forbidden():
    return flask.render_template('site/forbidden.html'), 403


def internal_server_error(exception):
    if isinstance(exception, PermissionDenied):
        return redirect(url_for('common.forbidden'))
    return flask.render_template('site/internal_server_error.html'), 500


def not_found(exception):
    return flask.render_template('site/not_found.html'), 404
