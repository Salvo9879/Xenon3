
# Import internal modules
from package.display import Colors, Objects
import package.package_handler as ph

# Import external modules
import socket
import urllib.request
import subprocess
import time
import os



# Variables
INTERNET_CONNECTIVITY_AWAIT_TIME = 3
SEQUENCE_AWAIT_TIME = 0.5
MAX_ATTEMPTS = 3

c = Colors()
o = Objects()



class Helpers():
    """ Holds all the helpers which might be needed to complete a test, solve or setup. """
    def _basic_requests(self, url: str, t: type = str) -> any:
        """ A basic version of the `requests` library (GET) that doesn't use external dependencies. """
        r: bytes = urllib.request.urlopen(url).read()
        dr = r.decode('utf-8')
        return t(dr)
    
    def get_required_dependencies(self) -> list:
        """ Returns a list of the required dependencies hosted on the `get_file_url`. """
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
    
    def get_invalid_db_paths(self) -> list:
        """ Gets a list of the `db-paths` which are relative or not configured as a sqlalchemy uri. """
        db_uris = ph.get_db_paths()

        db_ip = []
        for n in db_uris:
            v = db_uris[n]
            p = v[10:] if v[:10] == 'sqlite:///' else v # if the first 10 characters are `sqlite:///` then remove the first 10 characters. Else leave it
            if not os.path.isabs(p) or v[:10] != 'sqlite:///': # If that basic path is relative or does not start with `sqlite:///` then add it to the list
                db_ip.append([n, p])

        return db_ip
    
    def get_unformed_databases(self) -> list:
        """ Gets a list of all the databases created. """
        from sqlalchemy_utils import database_exists

        uf_dbs = []
        db_uris = ph.get_db_paths()
        for n in db_uris:
            p = db_uris[n]
            if not database_exists(p):
                uf_dbs.append([n, p])

        return uf_dbs



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
    
    def db_invalid_paths_test(self) -> bool:
        """ Tests whether all the database paths in the `package.json` file are absolute. """
        db_ip = self.h.get_invalid_db_paths()
        return (not db_ip)
    
    def db_creation_test(self):
        """ Test which tests if all databases has been created. """
        uf_db = self.h.get_unformed_databases()
        return not uf_db



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

    def solve_db_invalid_paths(self) -> None:
        """ Attempts to solve the database absolute paths test. """
        db_ip = self.h.get_invalid_db_paths()
        db_uris = ph.get_db_paths()

        for ip in db_ip:
            n, p = ip
            ap = os.path.abspath(p)
            ap = f"sqlite:///{ap}"

            db_uris[n] = ap

        ph.set_db_paths(db_uris)    

    def solve_db_creation(self):
        """ Attempts to solve the database creation test. """
        from package.databases import db
        from package.server import settings

        c.process(f"Attempting to create databases...")
        try:
            with settings.app_context():
                db.create_all()
        except Exception as e:
            c.caution(e)



class Setup():
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
        """ Sets up the machine for PIP installation. """
        t = self.t.pip_installation_test
        s = self.s.solve_pip_installation
        n = 'PIP Installation Test'

        self.base_setup(t=t, s=s, n=n)

    def dependency_installation_setup(self) -> None:
        """ Sets up the machine for dependency installation. """
        t = self.t.dependency_installation_test
        s = self.s.solve_dependency_installation
        n = 'Dependency Installation Test'

        self.base_setup(t=t, s=s, n=n)

    def db_abs_paths_setup(self) -> None:
        """ Sets up the `db-paths` in the `package.json` file to be absolute. """
        t = self.t.db_invalid_paths_test
        s = self.s.solve_db_invalid_paths
        n = 'Database Absolute Paths Test'

        self.base_setup(t=t, s=s, n=n)

    def db_creation_setup(self) -> None:
        """ Sets up the machine ready with created databases. """
        t = self.t.db_creation_test
        s = self.s.solve_db_creation
        n = 'Database Creation Test'

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
        self.db_abs_paths_setup()

        time.sleep(SEQUENCE_AWAIT_TIME)
        self.db_creation_setup()

        time.sleep(SEQUENCE_AWAIT_TIME)
        self.setup_successful()