
# Import internal modules
from package.validators import DataRequired, Email, EqualTo
from package.validators import InvalidUsername, IncorrectPassword, UniqueUsername, UniqueEmail, DayMonthMatch
from package.helpers import get_31, get_last_100_years

# Import external modules
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SelectField

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(), InvalidUsername()])
    password = PasswordField(validators=[DataRequired(), IncorrectPassword()])

class SignupForm(FlaskForm):
    forename = StringField(validators=[DataRequired()])
    surname = StringField(validators=[DataRequired()])

    username = StringField(validators=[DataRequired(), UniqueUsername()])
    email = EmailField(validators=[DataRequired(), Email(), UniqueEmail()])

    birthdate_day = SelectField(validators=[DataRequired(), DayMonthMatch()], choices=get_31())
    birthdate_month = SelectField(validators=[DataRequired()], choices=[i for i in range(1, 13)])
    birthdate_year = SelectField(validators=[DataRequired()], choices=get_last_100_years())

    password_alpha = PasswordField(validators=[DataRequired(), EqualTo('password_beta', message='Passwords do not match.')])
    password_beta = PasswordField(validators=[DataRequired(), EqualTo('password_alpha', message='Passwords do not match.')])