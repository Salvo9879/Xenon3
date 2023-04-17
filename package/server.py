
# Import internal modules
from package.databases import db, Users
from package.config import AppSettings
from package.applications_handler import ApplicationManager
from package.routes import api_r, authentication_r

import package.package_handler as ph

# Import external modules
from flask import Flask

# Variables
app = Flask(__name__)
settings = AppSettings()
application_manager = ApplicationManager()

# Application configuration
app.config['SECRET_KEY'] = settings.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = ph.get_db_paths()['users']
app.config['SQLALCHEMY_BINDS'] = {
    'applications': ph.get_db_paths()['applications']
}
app.template_folder = settings.template_folder
app.static_folder = settings.static_folder

# External configuration
db.init_app(app)
application_manager.register_applications_routes()

# Blueprint registration
app.register_blueprint(api_r)
app.register_blueprint(authentication_r)