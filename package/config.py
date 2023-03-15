
# Import internal modules
from package.display import Objects, Colors
 
import package.helpers as helpers

# Import external modules
import time

# Variables
MAX_ATTEMPTS = 3
AWAITING_TIME = 2
HOLD_TIME = 0.05

o = Objects()
c = Colors()

class Setup():
    """ Prepares the server for deployment. Attempts to solve any problem discovered, however raises an error if it fails. """
    def __init__(self, launch: bool = True) -> None:
        """ ## Params:
        `launch (bool) = False`: Should the setup sequence launch Xenon after a successful setup sequence. """
        
        self.launch = launch # Should the setup sequence launch Xenon after a successful setup sequence.
        self.failed_tests = [] # A list of failed tests. 

    def setup_failed(self, tn: str | list):
        """ Called if the system determines that the server has failed to set up the system. """
        if isinstance(tn, list):
            tn = '.'.join(tn)

        o.header(title='Setup failure', clr_scr=False)
        c.error(f"The setup sequence failed on: '{tn}'.")

    def setup_successful(self):
        """ Called if the system determines that the server has successfully set up the system. """
        o.header(title='Setup successful', clr_scr=False)
        c.success('The setup sequence has successfully been completed.')
        c.information('Xenon is now ready for deployment.')

        if self.launch:
            # Launch xenon
            pass

    def solve_internet_connectivity(self) -> bool:
        """ Attempts to solve a internet connectivity issue. Will hold awaiting for a connection, after 6 seconds (3 attempts, 2 seconds each), the setup process will exit. """
        time.sleep(HOLD_TIME)
        
        a = 0

        c.caution('( ! ) HOLD SETUP')
        c.process('- Attempting to solve the internet connectivity test.')

        s = False
        while a < MAX_ATTEMPTS:
            time.sleep(AWAITING_TIME)
            a += 1
            if not self.is_online(d=False):
                c.error(f"Attempt {a} failed...")
                continue
            c.error(f"Attempt {a} succeeded...")
            s = True
            break

        return s

    def solve_version_matching(self) -> bool:
        """ Doesn't solve the version matching problem. A version mismatch is when the current software is operating on an outdated version of Xenon. A simple update will fix this. """
        time.sleep(HOLD_TIME)
        
        c.caution('( ! ) HOLD SETUP')
        c.process('- The current software is operating on an outdated version of Xenon. Please update.')

        time.sleep(AWAITING_TIME)

        return True
    
    def solve_pip_configuration(self) -> bool:
        """ Attempts to install pip or update to the latest version. """
        time.sleep(HOLD_TIME)

        a = 0

        c.caution('( ! ) HOLD SETUP')
        c.process('- Attempting to solve PIP configuration test.')

        s = False
        while a < MAX_ATTEMPTS:
            time.sleep(AWAITING_TIME)

            a += 1

            helpers.download_pip()
            if self.is_pip_configured(d=False):
                c.success(f"Attempt {a} succeeded...")
                s = True
                break
            c.error(f"Attempt {a} failed...")

        return s
    
    def solve_dependency_loading_test(self) -> bool:
        """ Attempts to solve any uninstalled or outdated dependencies. Will attempt to install/update all system, however if fails after 3 attempts, the setup process will exit. """
        time.sleep(HOLD_TIME)

        a = 0

        c.caution('( ! ) HOLD SETUP')
        c.process('- Attempting to solve the dependency loading test.')

        s = False
        while a < MAX_ATTEMPTS:
            time.sleep(AWAITING_TIME)

            a += 1
            _, uip = self.dependencies_loaded(d=False)

            for p in uip:
                helpers.download_package(p)

            if self.dependencies_loaded(d=False)[0]:
                s = True
                c.success(f"Attempt {a} succeeded...")
                break

            c.caution(f"Attempt {a} failed...")
            continue

        return s
    
    def is_online(self, d: bool = True) -> bool:
        """ Returns a boolean based whether the machine is online. """
        res = helpers.is_online()

        if d:
            if res:
                c.success(f"[ {str(res).upper()} ] Internet connectivity test.")
                return res
            c.error(f"[ {str(res).upper()} ] Internet connectivity test.")
            return res

    def is_version_latest(self, d: bool = True) -> bool:
        """ Returns a boolean based whether the version of Xenon installed is the latest version. """
        opf = helpers.get_online_package_file()
        cpf = helpers.get_package_file()

        res = opf['version'] == cpf['version']

        if d:
            if res:
                c.success(f"[ {str(res).upper()} ] Version matching test.")
                return res
            c.error(f"[ {str(res).upper()} ] Version matching test.")
            return     

        return res
    
    def is_pip_configured(self, d: bool = True) -> bool:
        """ Tests whether pip is installed & if it is updated to the latest version. """
        res = helpers.is_pip_configured()

        if d:
            if res:
                c.success(f"[ {str(res).upper()} ] PIP configuration test.")
                return res
            
            c.error(f"[ {str(res).upper()} ] PIP configuration test.")
            return res

    def dependencies_loaded(self, d: bool = True) -> tuple:
        """ Tests to check whether all the required packages are installed & up to date onto the machine. """
        cp = helpers.get_all_packages()
        op = helpers.get_online_resource('requirements.txt').splitlines()

        uip = []
        for r in op:
            if not r in cp:
                uip.append(r)

        res = bool(not uip)

        if d:
            if res:
                c.success(f"[ {str(res).upper()} ] Dependency loading test.")
                return (res, uip)
            c.error(f"[ {str(res).upper()} ] Dependency loading test.")
            return (res, uip)
        return (res, uip)

    def run(self):
        """ This function tests for various conditions which are essential for the deployment of the server. """
        o.header(title='Running setup')

        time.sleep(HOLD_TIME)
        t1_r = s = self.is_online()
        if not t1_r:
            s = self.solve_internet_connectivity()
            if not s:
                self.setup_failed(tn='Internet connectivity test')
                return
        if not s:
            self.failed_tests.append('Internet connectivity test')

        time.sleep(HOLD_TIME)
        t2_r = s = self.is_version_latest()
        if not t2_r:
            s = self.solve_version_matching()
            if not s:
                self.setup_failed(tn='Version matching test')
                return
        if not s:
            self.failed_tests.append('Version matching test')
            
        time.sleep(HOLD_TIME)
        t3_r = s = self.is_pip_configured()
        if not t3_r:
            s = self.solve_pip_configuration()
            if not s:
                self.setup_failed(tn='PIP configuration test')
                return 
        if not s:
            self.failed_tests.append('PIP configuration test')

        time.sleep(HOLD_TIME)
        t4_r = s = self.dependencies_loaded()[0]
        if not t4_r:
            s = self.solve_dependency_loading_test()
            if not s:
                self.setup_failed(tn='Dependency loading test')
                return
        if not s:
            self.failed_tests.append('Dependency loading test')
        
        if not self.failed_tests:
            self.setup_successful()
            return
        self.setup_failed(tn=self.failed_tests)