
# Import internal modules
from package.display import Colors, Objects
import package.package_handler as ph

# Import external modules
import socket
import json
import urllib.request
import subprocess
import time
import os



# Variables
PACKAGE_FILE = 'package.json'
INTERNET_CONNECTIVITY_AWAIT_TIME = 3
SEQUENCE_AWAIT_TIME = 0.5
MAX_ATTEMPTS = 3

c = Colors()
o = Objects()



class Helpers():
    def _basic_requests(self, url: str, t: type = str) -> any:
        """ A basic version of the `requests` library (GET) that doesn't use external dependencies. """
        r: bytes = urllib.request.urlopen(url).read()
        dr = r.decode('utf-8')
        return t(dr)
    
    def _get_package_file_content(self) -> dict:
        """ Gets the content found in the `package.json` file. """
        with open(PACKAGE_FILE, 'r') as f:
            data = json.load(f)
        return data
    
    def get_required_dependencies(self) -> list:
        """ Returns a list of the required dependencies hosted on the `get_file_url`. """
        pfc = self._get_package_file_content()
        gf_url = ph.get_file_url()
        r_url = f"{gf_url}/requirements.txt"

        rdl = []
        olr: str = self._basic_requests(r_url, t=str)
        rdl.extend(olr.splitlines())

        return rdl
    
    def get_installed_dependencies(self) -> list:
        """ Gets all the dependencies installed onto the machine. """
        res = subprocess.run('pip freeze', text=True, capture_output=True)
        return res.stdout.splitlines()
    
    def get_uninstalled_dependencies(self) -> list:
        """ Gets a list of dependencies that should be installed but are not. """
        rds = self.get_required_dependencies()
        ids = self.get_installed_dependencies()

        uds = []
        for d in rds:
            if d not in ids:
                uds.append(d)

        return uds



class Tests():
    """ Holds all the tests that are required for the setup sequence. """
    def __init__(self) -> None:
        self.h = Helpers()

    def internet_connectivity_test(self) -> bool:
        """ Tests whether the machine is connected to the internet. """
        try:
            socket.setdefaulttimeout(3)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
            return True
        except socket.error:
            return False

    def pip_installation_test(self) -> bool:
        """ Tests whether PIP is installed on the machine. """
        #! Does not check whether this is the latest version of pip.
        try:
            import pip
            return True
        except ModuleNotFoundError:
            return False

    def dependency_installation_test(self) -> bool:
        """ Tests whether all required dependencies are installed & on the right versions. """
        uds = self.h.get_uninstalled_dependencies()
        return not uds
    
    def db_abs_paths_test(self) -> bool:
        """ Tests whether all the database paths in the `package.json` file are absolute. """
        db_uris = ph.get_db_paths()
        
        for n in db_uris:
            v = db_uris[n]
            if not os.path.isabs(v):
                return False
        return True



class Solvers():
    """ Holds all the solvers that can be used to solve failed tests in the setup sequence. """
    def __init__(self) -> None:
        self.h = Helpers()
        
    def base_solver(self, test: object, solver: object, n: str) -> bool:
        """ The bas solver for all solvers. """
        c.caution('\n( ! ) HOLD SETUP')
        c.process(f"- Attempting to solve the {n}...\n")

        a = 0
        s = False
        while a < MAX_ATTEMPTS:
            a += 1
            solver()
            if not test():
                c.error(f"Attempt {a} failed...")
                continue
            c.success(f"Attempt {a} succeeded...")
            s = True
            break
        return s

    def solve_internet_connectivity(self) -> None:
        """ Attempts to solve the internet connectivity test. """
        time.sleep(INTERNET_CONNECTIVITY_AWAIT_TIME)
    
    def solve_pip_installation(self) -> None:
        """ Attempts to solve the PIP installation test. """
        subprocess.run('python -m pip install --upgrade pip', shell=True)

    def solve_dependency_installation(self) -> None:
        """ Attempts to solve the dependency installation text. """
        uds = self.h.get_uninstalled_dependencies()
        for d in uds:
            # print(f"Downloading: {d}")
            c.process(f"Installing dependency: {d}...")
            subprocess.run(f"pip install {d}", capture_output=False)

    def solve_db_abs_paths_test(self) -> None:
        """ Attempts to solve the database absolute paths test. """
        n_dict = {}
        db_uris = ph.get_db_paths()
        for n in db_uris:
            # TODO: Create function that only gets paths which are not absolute.
            v = db_uris[n]
            abs_p = os.path.abspath(v)
            n_dict.update({n: abs_p})

        ph.set_db_paths(n_dict)



class PreSetup():
    """ A setup sequence which runs before the application is loaded. """
    def __init__(self) -> None:
        self.t = Tests()
        self.s = Solvers()

        self.ft = []
        self.ss = False

    def setup_failed(self, n: str):
        """ Raised when the setup sequence has failed. """
        self.ft.append(n)
        
        o.header(title='Setup failure', clr_scr=False)
        c.error(f"Setup failed on: {','.join(self.ft)}.")
        exit()

    def setup_successful(self) -> None:
        """ Runs when the Setup sequence is successful. """
        self.ss = True

        o.header('Setup successful', clr_scr=False)
        c.success('The setup sequence was successful. The server will now deploy!')

        time.sleep(SEQUENCE_AWAIT_TIME*4)

    def base_setup(self, t: any, s: any, n: str) -> None:
        """ The base setup for all setups. """

        tr = t()
        if not tr:
            c.error(f"[ {str(tr).upper()} ] - {n}.")
            su = self.s.base_solver(test=t, solver=s, n=n)
            if not su:
                self.setup_failed(n)
                return
            return
        c.success(f"[ {str(tr).upper()} ] - {n}.")

    def internet_connectivity_setup(self) -> None:
        """ Setups the machine for internet connectivity. """
        t = self.t.internet_connectivity_test
        s = self.s.solve_internet_connectivity
        n = 'Internet Connectivity Test'

        self.base_setup(t=t, s=s, n=n)

    def pip_installation_setup(self) -> None:
        """ Setups the machine for PIP installation. """
        t = self.t.pip_installation_test
        s = self.s.solve_pip_installation
        n = 'PIP Installation Test'

        self.base_setup(t=t, s=s, n=n)

    def dependency_installation_setup(self) -> None:
        """ Setups the machine for dependency installation. """
        t = self.t.dependency_installation_test
        s = self.s.solve_dependency_installation
        n = 'Dependency Installation Test'

        self.base_setup(t=t, s=s, n=n)

    def db_abs_paths_test(self) -> None:
        """ Set ups the `db-paths` in the `package.json` file to be absolute. """
        t = self.t.db_abs_paths_test
        s = self.s.solve_db_abs_paths_test
        n = 'Database Absolute Paths Tests'

        self.base_setup(t=t, s=s, n=n)
            
    def run(self) -> None:
        """ Runs the entire setup sequence. """

        o.header(title='Setup sequence')
        c.process('Setting up the machine for Xenon...\n')

        time.sleep(SEQUENCE_AWAIT_TIME)
        self.internet_connectivity_setup()

        time.sleep(SEQUENCE_AWAIT_TIME)
        self.pip_installation_setup()

        time.sleep(SEQUENCE_AWAIT_TIME)
        self.dependency_installation_setup()

        time.sleep(SEQUENCE_AWAIT_TIME)
        self.db_abs_paths_test()

        self.setup_successful()