
# Import internal modules
from package.databases import db
from package.config import AppSettings

import package.package_handler as ph

# Import external modules
from flask import Flask

# Variables
app = Flask(__name__)
settings = AppSettings()
# Application configuration
app.config['SECRET_KEY'] = settings.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = ph.get_db_paths()['users']

# External configuration
db.init_app(app)
