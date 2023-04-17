
# Import internal modules
from package.forms import LoginForm
from package.databases import Users

# Import external modules
from flask import Blueprint, render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import current_user, login_user, logout_user, login_required

# Blueprint declaration
authentication_r = Blueprint('authentication', __name__, url_prefix='/authentication')
authentication_formrequests = Blueprint('authentication', __name__, url_prefix='/authentication') # api.formrequest.authentication_api

# Routes (authentication)
@authentication_r.route('/login')
def login():
    """ The page which helps the user to log into their profile. """
    lf = LoginForm()

    username_state, password_state = '', ''
    username_error_msg, password_error_msg, general_error_msg = '', '', None
    print(get_flashed_messages())
    for message in get_flashed_messages():
        for error_name in message:
            
            if error_name == 'username':
                username_state = 'error'
                username_error_msg = message[error_name][0]

            if error_name == 'password':
                password_state = 'error'
                password_error_msg = message[error_name][0]

            if error_name == 'general':
                general_error_msg = message[error_name]

    return render_template('templates/pages/authentication/login1.html', lf=lf, us=username_state, ps=password_state, uem=username_error_msg, pem=password_error_msg, gem=general_error_msg)

@authentication_r.route('/logout')
@login_required
def logout():
    """ Logs out the current user, then redirects to the login page. """
    logout_user()
    return redirect(url_for('authentication.login'))

@authentication_r.route('/signup')
def signup():
    return 

# Routes (api.formrequests.authentication)
@authentication_formrequests.route('/login_fr', methods=['POST'])
def login_fr():
    """ The api formrequests endpoint which handles the logging process. """
    lf = LoginForm()

    if lf.validate_on_submit():
        u = Users.query.filter_by(username=lf.username.data).first()

        s = login_user(u)
        if not s:
            flash({'general': 'There was a problem logging into your account.'})
            return redirect(url_for('authentication.login'))
        
        return redirect(url_for('')) # Enter endpoint of the dashboard.

    flash(lf.errors)
    return redirect(url_for('authentication.login'))

@authentication_formrequests.route('/signup')
def signup_fr():
    return