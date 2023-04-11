class ApplicationAlreadyPinned(Exception):
    """ Raised when the user attempts to pin an app where its uuid is already listed in the database. Returns the app uuid. """
    pass