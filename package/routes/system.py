
# Import internal modules
from package.system_handler import system

# Import external modules
from flask import Blueprint, jsonify

system_api = Blueprint('system', __name__, url_prefix='system')

@system_api.route('/datetime')
def datetime():
    return jsonify({
        'date': system.datetime.current_date,
        'time': system.datetime.current_time
    })