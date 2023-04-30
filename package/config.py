
# Import internal modules
from package.display import Colors, Objects
from package.package_handler import get_app_settings_path

# Import external modules
from configparser import ConfigParser

import os

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

        self.template_folder = os.path.abspath('package/site')
        self.static_folder = os.path.abspath('package/site')

class DateTimeConfig():
    def __init__(self, fp: str | None = None) -> None:
        if fp is None:
            fp = get_app_settings_path()
        self.fp = fp

        self.cp = ConfigParser()
        self.cp.read(self.fp)

        self.date_order = self.cp.get('DATETIME', 'date_order')
        self.date_day_format = self.cp.getint('DATETIME', 'date_day_format')
        self.date_month_format = self.cp.getint('DATETIME', 'date_month_format')
        self.date_year_format = self.cp.getint('DATETIME', 'date_year_format')
        self.time_format = self.cp.getint('DATETIME', 'time_format')

    def write(self, date_order: str, date_day_format: int, date_month_format: int, date_year_format: int, time_format) -> None:
        """ Overrides the currently stored values for given ones. """

        self.cp.set('DATETIME', 'date_order', date_order)
        self.cp.set('DATETIME', 'date_day_format', date_day_format)
        self.cp.set('DATETIME', 'date_month_format', date_month_format)
        self.cp.set('DATETIME', 'date_year_format', date_year_format)
        self.cp.set('DATETIME', 'time_format', time_format)

        with open(self.fp, 'wb') as f:
            self.cp.write(f)