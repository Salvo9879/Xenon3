
# Import internal modules
from package.exceptions import ApplicationAlreadyPinned, NotificationReceivedAgain
from package.notifications import Notification

import package.helpers as helpers

# Import external modules
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Variables
db = SQLAlchemy()

class Users(db.Model, UserMixin):
    """ A database which stores information about the user profiles. """
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False, default=helpers.get_uuid())

    forename = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)

    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)

    birthdate = db.Column(db.String, nullable=False)
    creation_date = db.Column(db.String, nullable=False, default=helpers.get_iso_dt())

    hashed_password = db.Column(db.String, nullable=False)

    pinned_apps = db.Column(db.PickleType, nullable=False, default=[])

    notification_box = db.Column(db.PickleType, nullable=False, default=[])

    @property
    def password(self) -> AttributeError:
        """ Raises an error if the application attempts to read the attribute. """
        raise AttributeError('Cannot read attribute \'password\'')
    
    @property
    def notification_box_empty(self) -> bool:
        """ Returns `True` if the notification box is empty. """
        return not self.notification_box
    
    @password.setter
    def password(self, pwd: str) -> None:
        """ Converts the given password into a hashed version & stores it in the instance. """
        self.hashed_password = generate_password_hash(pwd)

    def verify_password(self, pwd: str) -> bool:
        """ Returns a boolean based on if a given text-based password is correct based on a hashed version. """
        return check_password_hash(self.hashed_password, pwd)
    
    def pin_app(self, app_uuid: str) -> None:
        """ Adds an app uuid to the pinned apps column. """
        pa = self.pinned_apps.copy()

        if app_uuid in pa:
            raise ApplicationAlreadyPinned(app_uuid)

        pa.append(app_uuid)
        self.pinned_apps = pa

        db.session.commit()

    def unpin_app(self, app_uuid: str) -> None:
        """ Removes an app uuid from the pinned apps column. """
        pa = self.pinned_apps

        if not app_uuid in pa:
            return
        
        pa.remove(app_uuid)
        self.pinned_apps = pa

        db.session.commit()

    def add_notification(self, n: Notification) -> None:
        """ Adds a `package.notifications.Notifications` object to the users notification box. """
        nb = self.notification_box.copy()

        for no in nb:
            if no.notification_uuid == n.notification_uuid:
                raise NotificationReceivedAgain(n.notification_uuid)
            
        nb.append(n)
        self.notification_box = nb

        db.session.commit()

    def delete_notification(self, notification_uuid: str) -> None:
        """ Deletes a `package.notifications.Notifications` object from the users notification box. """
        nb = self.notification_box.copy()

        for i, no in enumerate(nb):
            if no.notification_uuid == notification_uuid:
                nb.pop(i)

        self.notification_box = nb

        db.session.commit()


class Applications(db.Model):
    """ A database which stores information about applications stored on the Xenon system """
    __bind_key__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String, nullable=False, unique=True)

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False)

    developers = db.Column(db.String, nullable=False)
    icon_path = db.Column(db.String, nullable=False)