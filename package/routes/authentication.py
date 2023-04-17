
# Import internal modules

# Import external modules
from flask import Blueprint
from flask_login import current_user, logout_user

# Blueprint declaration
authentication_r = Blueprint('authentication', __name__, url_prefix='/authentication')
authentication_formrequests = Blueprint('authentication_formrequests', __name__, url_prefix='/authentication') # api.formrequest.authentication_api

# Routes (authentication)
@authentication_r.route('/login')
def login():
    return

@authentication_r.route('/logout')
def logout():
    return

@authentication_r.route('/signup')
def signup():
    return 

# Routes (api.formrequests.authentication)
@authentication_formrequests.route('/login')
def login_fr():
    return

@authentication_formrequests.route('/logout')
def logout_fr():
    return

@authentication_formrequests.route('/signup')
def signup_fr():
    return