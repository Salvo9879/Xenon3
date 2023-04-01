
# Import internal modules
import package.helpers as helpers

# Import external modules
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Variables
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False, default=helpers.get_uuid())

    forename = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)

    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)

    birthdate = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.String, nullable=False, default=helpers.get_iso_dt())

    hashed_password = db.Column(db.String, nullable=False)

    @property
    def password(self) -> AttributeError:
        """ Raises an error if the application attempts to read the attribute. """
        raise AttributeError('Cannot read attribute \'password\'')
    
    @password.setter
    def password(self, pwd: str) -> None:
        """ Converts the given password into a hashed version & stores it in the instance. """
        self.hashed_password = generate_password_hash(pwd)

    def verify_password(self, pwd: str) -> bool:
        """ Returns a boolean based on if a given text-based password is correct based on a hashed version. """
        return check_password_hash(pwd)