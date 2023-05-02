""" 
Categories:
    - System > Operating system > Python download > Dependencies
    - Storage
    - Hardware
    - Internet
    - Server 
    - Customization
    - Security
    - Logs
    - Activity
    - User settings
    - Notifications
    - Statistics
    - Support
    - Focuses
"""

# Import external modules
from flask import Blueprint

# Blueprint declaration
settings_r = Blueprint('settings', __name__, url_prefix='/settings')

# Routes
@settings_r.route('/')
def index():
    return 'Success'