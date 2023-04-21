
# Import internal modules
from package.databases import Users
from package.helpers import MONTHS_DAY_DATA, MONTH_INDEXED_DATA

# Import external modules
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class InvalidUsername():
    """ Used only when logging in on the username field. Checks if a provided username is stored in the database. """
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'An account with this username does not exist.'
        self.message = message

    def __call__(self, _, field) -> None | ValidationError:
        u = Users.query.filter_by(username=field.data).first()
        if u is None:
            raise ValidationError(self.message)

class IncorrectPassword():
    """ Used only when logging in on the email field. Checks if a provided email is stored in the database. """
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'The password provided is incorrect.'
        self.message = message

    def __call__(self, form, field) -> None | ValidationError:
        u = Users.query.filter_by(username=form.username.data).first()
        if u is None:
            return
        
        if not u.verify_password(field.data):
            raise ValidationError(self.message)
        
class UniqueUsername():
    """ Used only when signing up on the username field. Checks if a provided username is unique. """
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'An account with this username already exists.'
        self.message = message

    def __call__(self, _, field,) -> None | ValidationError:
        u = Users.query.filter_by(username=field.data).first()
        if not u is None:
            raise ValidationError(self.message)
        
class UniqueEmail():
    """ Used only when signing up on the email field. Checks if a provided email is unique. """
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'An account with this email already exists.'
        self.message = message

    def __call__(self, _, field,) -> None | ValidationError:
        u = Users.query.filter_by(email=field.data).first()
        if not u is None:
            raise ValidationError(self.message)
        
class DayMonthMatch():
    """ Checks if the users birthdate day matches it largest day in its month. Example will raise a `ValidationError` if the user enters day `31` on `February`. """
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'The amount days given does not match the month provided.'
        self.message = message

    def __call__(self, form, field) -> None | ValidationError:
        bdm = int(form.birthdate_month.data)
        bdd = int(field.data)

        if not MONTHS_DAY_DATA[MONTH_INDEXED_DATA[bdm-1]] > bdd:
            raise ValidationError(self.message)