
# Import internal modules
from package.databases import Users
from package.helpers import MONTHS_DAY_DATA, MONTH_INDEXED_DATA

# Import external modules
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

class InvalidUsername():
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'An account with this username does not exist.'
        self.message = message

    def __call__(self, _, field) -> None | ValidationError:
        u = Users.query.filter_by(username=field.data).first()
        if u is None:
            raise ValidationError(self.message)

class IncorrectPassword():
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
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'An account with this username already exists.'
        self.message = message

    def __call__(self, _, field,) -> None | ValidationError:
        u = Users.query.filter_by(username=field.data).first()
        if not u is None:
            raise ValidationError(self.message)
        
class UniqueEmail():
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'An account with this email already exists.'
        self.message = message

    def __call__(self, _, field,) -> None | ValidationError:
        u = Users.query.filter_by(email=field.data).first()
        if not u is None:
            raise ValidationError(self.message)
        
class DayMonthMatch():
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'The amount days given does not match the month provided.'
        self.message = message

    def __call__(self, form, field) -> None | ValidationError:
        bdm = int(form.birthdate_month.data)
        bdd = int(field.data)

        if not MONTHS_DAY_DATA[MONTH_INDEXED_DATA[bdm-1]] > bdd:
            raise ValidationError(self.message)