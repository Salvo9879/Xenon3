
# Import internal modules
from package.databases import Users

# Import external modules
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired

class InvalidUsername():
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'An account with this username does not exist.'
        self.message = message

    def __call__(self, _, field):
        u = Users.query.filter_by(username=field.data).first()
        if u is None:
            raise ValidationError(self.message)

class IncorrectPassword():
    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = 'The password provided is incorrect.'
        self.message = message

    def __call__(self, form, field):
        u = Users.query.filter_by(username=form.username.data).first()
        if u is None:
            return
        
        if not u.verify_password(field.data):
            raise ValidationError(self.message)