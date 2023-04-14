
# Import internal modules
from flask import Blueprint

applications_r = Blueprint('applications', __name__, url_prefix='/application')

@applications_r.route('/y')
def y():
    return 'yyyy'