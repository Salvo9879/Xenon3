class ApplicationAlreadyPinned(Exception):
    """ Raised when the user attempts to pin an app where its uuid is already listed in the database. Returns the app uuid. """
    pass

class ApplicationUnavailable(Exception):
    """ Raised when the system checks for an application at the Xenon server, however the referenced github repo is invalid or if the app uuid isn't even referenced by the Xenon application servers. """
    pass