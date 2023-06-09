class ApplicationAlreadyPinned(Exception):
    """ Raised when the user attempts to pin an app where its uuid is already listed in the database. Returns the app uuid. """
    pass

class ApplicationUnavailable(Exception):
    """ Raised when the system checks for an application at the Xenon server, however the referenced github repo is invalid or if the app uuid isn't even referenced by the Xenon application servers. """
    pass

class ApplicationNotInstalled(Exception):
    """ Raised when the system is attempting to access data from an application that is not installed on the Xenon system. """
    pass

class NotificationReceivedAgain(Exception):
    """ Raised when a notification is sent to the users notification box, however that notification has already been received. """
    pass