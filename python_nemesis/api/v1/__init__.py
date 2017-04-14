from flask import Blueprint
from flask import jsonify
from python_nemesis.exceptions import general_handler
from python_nemesis.exceptions import NemesisException


V1_API = Blueprint('v1_api', __name__)


@V1_API.errorhandler(NemesisException)
def handle_exception(error):
    return general_handler(error)


@V1_API.route('/v1')
def api_definition():
    return ""
