
# Import internal modules
from package.forms import LoginForm, SignupForm
from package.databases import Users
from package.users import create_user

import package.helpers as helpers

# Import external modules
from flask import Blueprint, render_template, redirect, url_for, flash, get_flashed_messages
from flask_login import current_user, login_user, logout_user, login_required

import datetime

# Blueprint declaration
authentication_r = Blueprint('authentication', __name__, url_prefix='/authentication')
authentication_formrequests = Blueprint('authentication', __name__, url_prefix='/authentication') # api.formrequest.authentication_api

# Routes (authentication)
@authentication_r.route('/login')
def login():
    """ The page which helps the user to log into their profile. """

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    lf = LoginForm()

    username_state, password_state = '', ''
    username_error_msg, password_error_msg, general_error_msg = '', '', None

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

    return render_template('templates/pages/authentication/login.html', lf=lf, username_state=username_state, password_state=password_state, username_error_msg=username_error_msg, password_error_msg=password_error_msg, general_error_msg=general_error_msg)

@authentication_r.route('/logout')
@login_required
def logout():
    """ Logs out the current user, then redirects to the login page. """
    logout_user()
    return redirect(url_for('authentication.login'))

@authentication_r.route('/signup')
def signup():
    """ The page which helps the user to sign up to Xenon. """

    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    sf = SignupForm()

    forename_state, surname_state, username_state, email_state, birthdate_day_state, birthdate_month_state, birthdate_year_state, password_alpha_state, password_beta_state = '', '', '', '', '', '', '', '', ''
    forename_error_msg, surname_error_msg, username_error_msg, email_error_msg, birthdate_day_error_msg, birthdate_month_error_msg, birthdate_year_error_msg, password_alpha_error_msg, password_beta_error_msg, general_error_msg = '', '', '', '', '', '', '', '', '', None
    
    for message in get_flashed_messages():
        for error_name in message:

            if error_name == 'forename':
                forename_state = 'error'
                forename_error_msg = message[error_name][0]

            if error_name == 'surname':
                surname_state = 'error'
                surname_error_msg = message[error_name][0]

            if error_name == 'username':
                username_state = 'error'
                username_error_msg = message[error_name][0]

            if error_name == 'email':
                email_state = 'error'
                email_error_msg = message[error_name][0]

            if error_name == 'birthdate_day':
                birthdate_day_state = 'error'
                birthdate_day_error_msg = message[error_name][0]

            if error_name == 'birthdate_month':
                birthdate_month_state = 'error'
                birthdate_month_error_msg = message[error_name][0]

            if error_name == 'birthdate_year':
                birthdate_year_state = 'error'
                birthdate_year_error_msg = message[error_name][0]

            if error_name == 'password_alpha':
                password_alpha_state = 'error'
                password_alpha_error_msg = message[error_name][0]

            if error_name == 'password_beta':
                password_beta_state = 'error'
                password_beta_error_msg = message[error_name][0]

            if error_name == 'general':
                general_error_msg = message[error_name]

    return render_template(
        'templates/pages/authentication/signup.html', sf=sf, 
        forename_state=forename_state, surname_state=surname_state, username_state=username_state, email_state=email_state, birthdate_day_state=birthdate_day_state, birthdate_month_state=birthdate_month_state, birthdate_year_state=birthdate_year_state, password_alpha_state=password_alpha_state, password_beta_state=password_beta_state,
        forename_error_msg=forename_error_msg, surname_error_msg=surname_error_msg, username_error_msg=username_error_msg, email_error_msg=email_error_msg, birthdate_day_error_msg=birthdate_day_error_msg, birthdate_month_error_msg=birthdate_month_error_msg, birthdate_year_error_msg=birthdate_year_error_msg, password_alpha_error_msg=password_alpha_error_msg, password_beta_error_msg=password_beta_error_msg, general_error_msg=general_error_msg
    )



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
        
        return redirect(url_for('dashboard.index'))

    flash(lf.errors)
    return redirect(url_for('authentication.login'))

@authentication_formrequests.route('/signup', methods=['POST'])
def signup_fr():
    """ The api formrequests endpoint which handles the signing up process. """
    sf = SignupForm()

    if sf.validate_on_submit():
        birthdate = helpers.get_iso_dt(datetime.datetime(year=int(sf.birthdate_year.data), month=int(sf.birthdate_month.data), day=int(sf.birthdate_day.data)))
        u = create_user(
            forename=sf.forename.data, surname=sf.surname.data,
            username=sf.username.data, email=sf.email.data,
            birthdate=birthdate, password=sf.password_beta.data
        )

        if u is None:
            flash({'general': 'There was a problem creating your account. Please try again later.'})
            return redirect(url_for('authentication.signup'))

        s = login_user(u)
        if not s:
            flash(flash({'general': 'There was a problem logging into your account. Your account was created.'}))
            return redirect(url_for('authentication.login'))
        
        return redirect(url_for('dashboard.index'))

    flash(sf.errors)
    return redirect(url_for('authentication.signup'))