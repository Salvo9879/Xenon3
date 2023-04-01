
# Import internal modules
from package.display import Colors, Objects

from package.package_handler import get_app_settings_path

# Import external modules
from configparser import ConfigParser

# Variables 
c = Colors()
o = Objects()

class AppSettings():
    """ A instance which holds all the information regarding the applications settings. """
    def __init__(self, fp: str | None = None) -> None:
        if fp is None:
            fp = get_app_settings_path()
        self.fp = fp

        cp = ConfigParser()
        cp.read(self.fp)

        # Deployment
        self.host = cp.get('DEPLOYMENT', 'host')
        self.port = cp.get('DEPLOYMENT', 'port')
        self.debug = cp.get('DEPLOYMENT', 'debug')

        # Application
        self.secret_key = cp.get('APPLICATION', 'secret_key')