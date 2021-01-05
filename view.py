from flask import jsonify, request, render_template, Blueprint

from error_handler import ErrorHandler
from request_handler import RequestHandler

view = Blueprint('view', __name__, url_prefix='')


@view.route('/')
def welcome():
    return render_template('splash.html')


@view.route('/search', methods=['POST'])
def search():
    try:
        # Process request and return final list json objects
        return jsonify(RequestHandler.process_request(request))
    except Exception as e:
        return jsonify({'ERROR': str(e)})
