
# Import internal modules
from package.databases import db, Users
from package.config import AppSettings
from package.applications_handler import ApplicationManager
from package.system_handler import system
from package.routes import api_r, applications_r, pages_r

import package.package_handler as ph
import package.helpers

# Import external modules
from flask import Flask
from flask_login import LoginManager

# Variables
app = Flask(__name__)
login_manager = LoginManager()
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
login_manager.init_app(app)
application_manager.register_applications_routes()
system.init_settings(settings)

# Blueprint registration
app.register_blueprint(api_r)
app.register_blueprint(applications_r)
app.register_blueprint(pages_r)

# User loader
@login_manager.user_loader
def load_user(user_id: str) -> Users:
    return Users.query.get(int(user_id))

# Context processors
@app.context_processor
def inject_helpers():
    """ Injects `package.helpers` into all jinja templating. """
    return dict(h=package.helpers)

@app.context_processor
def inject_system():
    """ Injects the `package.server.system` into all jinja templating. """
    return dict(system=system)