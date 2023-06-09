
# Import internal modules
from package.routes.authentication import authentication_formrequests
from package.routes.system import system_api

# Import external modules
from flask import Blueprint

# Blueprint declaration
api_r = Blueprint('api', __name__, url_prefix='/api')
formrequests_r = Blueprint('formrequests', __name__, url_prefix='/formrequests')

# Register blueprints
api_r.register_blueprint(formrequests_r)

api_r.register_blueprint(system_api)

formrequests_r.register_blueprint(authentication_formrequests)