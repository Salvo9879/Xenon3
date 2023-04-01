
# Import external modules
import uuid
import datetime

def get_uuid() -> str:
    """ Returns a string universally unique identifier. """
    u = uuid.uuid4()
    return str(u)

def get_dt_now() -> datetime.datetime:
    """ Returns the current datetime. """
    return datetime.datetime.now()

def get_iso_dt() -> str:
    """ Returns a string of the current datetime in a 8601 ISO format. """
    dt = get_dt_now()
    return dt.isoformat()