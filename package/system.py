
# Import internal modules
from package.config import AppSettings, DateTimeConfig

# Import external modules
import platform
import subprocess
import shutil
import psutil
import socket
import datetime

class OperatingSystem():
    @property
    def system_name(self) -> str:
        """ Returns the OS name. """
        return platform.system()
    
    @property
    def system_version(self) -> str:
        """ Returns the OS version. """
        return platform.version()
    
    @property
    def system_release(self) -> str:
        """ Returns the OS release. """
        return platform.release()

class PythonDownload():
    @property
    def python_compiler(self) -> str:
        """ Returns the python download compiler. """
        return platform.python_compiler()
    
    @property
    def python_implementation(self) -> str:
        """ Returns the python download implementation. """
        return platform.python_implementation()
    
    @property
    def python_version(self) -> str:
        """ Returns the python download version. """
        return platform.python_version()
    
class Dependencies():
    @property
    def dependencies_installed(self) -> list:
        """ Returns a list of the total dependencies installed on the machine. """
        res = subprocess.run('pip freeze', text=True, capture_output=True)
        return res.stdout.splitlines()
    
class Storage():
    @property
    def total_storage(self) -> int:
        """ Returns the total size of the storage device in bytes. """
        return shutil.disk_usage('/')[0]

    @property
    def used_storage(self) -> int:
        """ Returns the used size of the storage device in bytes. """
        return shutil.disk_usage('/')[1]
    
    @property
    def free_storage(self) -> int:
        """ Returns the free size of the storage device in bytes. """
        return shutil.disk_usage('/')[2]
    
class Hardware():
    @property
    def machine_type(self) -> str:
        """ Returns the machine type. """
        return platform.machine()
    
    @property
    def node(self) -> str:
        """ Returns the computer network name. """
        return platform.node()
    
    @property
    def processor(self) -> str:
        """ Returns the processor name. """
        return platform.processor()
    
    @property
    def logical_processors(self) -> int:
        """ Returns the amount of logical CPUs in the system. """
        return psutil.cpu_count()

    @property
    def processor_speed(self) -> float:
        """ Returns the clock speed of the processor in MHz. """
        return psutil.cpu_freq()[0]
    
    @property
    def processor_utilization(self) -> float:
        """ Returns the percentage utilization of the processor. Will return `0.0` on the first attempt. """
        return psutil.cpu_percent()
    
class Internet():
    @property
    def is_connected(self) -> bool:
        """ Returns a bool based on whether the machine is able to access information from a WAN. """
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
            return True
        except socket.error:
            return False
        
    @property
    def hostname(self) -> str:
        """ Returns the hostname of the machine. """
        return socket.gethostname()
        
    @property
    def ip_addr(self) -> str:
        """ Returns the local ip address of the machine. """
        return socket.gethostbyname(self.hostname)
    
class Server():
    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings

    @property
    def host(self) -> str:
        """ Returns the server host. """
        return self._settings.host
    
    @property
    def port(self) -> int:
        """ Returns the server port. """
        return self._settings.port
    
    @property
    def debug(self) -> bool:
        """ Returns the server debug mode. """
        return self._settings.debug
    
class DateTime():
    DATE_DAY_FORMAT = [
        ['%d', 'Day as a number - 01-31.'],
    ]
    DATE_MONTH_FORMAT = [
        ['%m', 'Month as a number - 01-12.'],
        ['%b', 'Month name - short version.'],
        ['%B', 'Month name - full version.']
    ]
    DATE_YEAR_FORMAT = [
        ['%y', 'Year number - short version.'],
        ['%Y', 'Year number - full version.']
    ]

    TIME_FORMAT = [
        ['%H:%M:%S', '24 hour with hours, minutes & seconds.'],
        ['%H:%M', '24 hour with hours & minutes.'],
        ['%I:%M:%S', '12 hour with hours, minutes & seconds. AM/PM not included.'],
        ['%I:%M', '12 hour with hours & minutes. AM/PM not included.'],
        ['%I:%M:%S %p', '12 hour with hours, minutes & seconds. AM/PM included.'],
        ['%I:%M %p', '12 hour with hours & minutes. AM/PM included.'],
    ]

    def __init__(self) -> None:
        self.update()

    def update(self) -> None:
        self.dtc = DateTimeConfig()

        self.date_order = self.dtc.date_order
        self.date_day_format = self.dtc.date_day_format
        self.date_month_format = self.dtc.date_month_format
        self.date_year_format = self.dtc.date_year_format

        self.date_format_technical = {
            'D': self.DATE_DAY_FORMAT[self.date_day_format],
            'M': self.DATE_MONTH_FORMAT[self.date_month_format],
            'Y': self.DATE_YEAR_FORMAT[self.date_year_format]
        }
        self.date_separator_symbol = ' '
        if self.date_month_format == 0:
            self.date_separator_symbol = '/'

        df_t = []
        for df in self.date_order:
            df_t.append(self.date_format_technical[df][0])

        self.date_format = self.date_separator_symbol.join(df_t)
        self.time_format = self.TIME_FORMAT[self.dtc.time_format][0]

    def save(self) -> None:
        """ Saves the current datetime settings to secondary storage. """
        self.dtc.write(self.date_order, self.date_day_format, self.date_month_format, self.date_year_format, self.time_format)

    @property
    def _current_dt(self) -> datetime.datetime:
        """ Returns a current `datetime.datetime` object. """
        return datetime.datetime.now()

    @property
    def current_time(self) -> str:
        n = self._current_dt
        return n.strftime(self.time_format)
    
    @property
    def current_date(self) -> str:
        n = self._current_dt
        return n.strftime(self.date_format)


class System():
    """ Holds information about the Xenon machine.
        1. Operating system information.
            a) System name. 
            b) System version.
            c) System release.

        2. Python download information.
            a) Python compiler.
            b) Python implementation.
            c) Python version

        3. Dependencies information.
            a) Downloaded dependencies

        4. Storage information.
            a) Total secondary storage space.
            b) Used secondary storage space.
            c) Free secondary storage space.

        5. Hardware information.
            a) Machine type
            b) Machine node
            c) Processor name
            d) Processor usage
            e) Memory usage.

        6. Internet information. 
            a) Connected to the internet. 
            b) Hostname.
            c) Local IP address. 

        7. Server information.
            a) Host.
            b) Port.
            c) Debug mode.
        """
    def __init__(self) -> None:
        self.operation_system = OperatingSystem()
        self.python_download = PythonDownload()
        self.dependencies = Dependencies()
        self.storage = Storage()
        self.hardware = Hardware()
        self.internet = Internet()
        self.datetime = DateTime()

    def init_settings(self, settings: AppSettings) -> None:
        """ Initializes the settings into the object. """
        self.server = Server(settings)