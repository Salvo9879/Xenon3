
# Import internal modules
from package.validators import DataRequired, InvalidUsername, IncorrectPassword

# Import external modules
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField

class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(), InvalidUsername()])
    password = PasswordField(validators=[DataRequired(), IncorrectPassword()])