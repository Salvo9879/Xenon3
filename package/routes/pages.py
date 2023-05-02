
# Import internal modules
from package.routes.authentication import authentication_r
from package.routes.dashboard import dashboard_r
from package.routes.settings import settings_r

# Import external modules
from flask import Blueprint

# Blueprint declaration
pages_r = Blueprint('pages', __name__)

# Register blueprints
pages_r.register_blueprint(authentication_r)
pages_r.register_blueprint(dashboard_r)
pages_r.register_blueprint(settings_r)