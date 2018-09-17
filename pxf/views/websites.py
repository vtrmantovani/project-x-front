import flask
from flask import Blueprint, jsonify, request
from flask_login import login_required

from pxf.backends.website import WebsiteBackend
from pxf.forms import WebsiteForm

bp_websites = Blueprint('websites', __name__, url_prefix='/websites')


@bp_websites.route('/', methods=['GET'])
@login_required
def index():
    return flask.render_template('website/list.html')


@bp_websites.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    website_form = WebsiteForm()
    if request.method == 'POST':
        if website_form.validate_on_submit():
            website_backend = WebsiteBackend()
            try:
                website_backend.create_website(website_form.data['url'])
                return flask.render_template('website/list.html')
            except Exception as e:
                flask.flash('Erro ao cadastrar url', 'error')

    return flask.render_template('website/create.html', form=website_form)


@bp_websites.route('/search', methods=['GET'])
@login_required
def search():
    status = 'DONE'
    limit = request.args.get('length')
    offset = request.args.get('start')

    website_backend = WebsiteBackend()
    response = website_backend.search(status, limit, offset)
    return jsonify(
        {'data': response['websites'],
         'draw': request.args.get('draw'),
         'recordsTotal': response['total_itens'],
         'recordsFiltered': response['total_itens']
         }
    )


@bp_websites.route('/show', methods=['GET'])
@bp_websites.route('/show/<website_id>', methods=['GET'])
@login_required
def show(website_id):
    website_backend = WebsiteBackend()
    website = website_backend.get_website(website_id)
    return flask.render_template('website/show.html', website=website)
