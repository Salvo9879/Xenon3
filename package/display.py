
# Import external modules
import os

# Variables
DEFAULT_HEADER_SIZE = 100
try:
    HEADER_SIZE = os.get_terminal_size()[0]
except:
    HEADER_SIZE = DEFAULT_HEADER_SIZE

class Colors():
    """ Colors which can be used to colorize terminal elements. """
    def __init__(self) -> None:
        if self.colorama_installed:
            import colorama
            self.f = colorama.Fore
            self.b = colorama.Back
            self.s = colorama.Style

    @property
    def point(self):
        if self.colorama_installed:
            p = {
                'fR': self.f.RED, # Error
                'fG': self.f.GREEN, # Success
                'fY': self.f.YELLOW, # Caution
                'fB': self.f.BLUE, # Instructions
                'fM': self.f.MAGENTA, # Process
                'fC': self.f.CYAN, # Title
                'fW': self.f.WHITE, # Information
                'fX': self.f.RESET, # Reset

                # Styles
                'sN': self.s.NORMAL, # Normal
                'sB': self.s.BRIGHT, # Bright
                'sX': self.s.RESET_ALL, # Reset
            }
        else:
            p = {'fR': '','fG': '','fY': '','fB': '','fM': '','fC': '','fW': '','fX': '','sN': '','sB': '','sX': ''}
        
        return p
    
    @property
    def colorama_installed(self):
        """ Returns a boolean based whether if the module `colorama` is installed. """
        try:
            import colorama
            return True
        except ModuleNotFoundError:
            return False
        
    def colored_print(self, conf_t: str) -> None:
        """ Base function for printing coloured text """
        p = self.point
        print(f"{conf_t}{p['sX']}{p['fX']}")
        
    def error(self, msg: str) -> None:
        """ Prints text with color for errors. """
        p = self.point
        self.colored_print(f"{p['fR']}{msg}")

    def success(self, msg: str) -> None:
        """ Prints text with color for success. """
        p = self.point
        self.colored_print(f"{p['fG']}{msg}")

    def caution(self, msg: str) -> None:
        """ Prints text with color for caution. """
        p = self.point
        self.colored_print(f"{p['fY']}{msg}")

    def instruction(self, msg: str) -> None:
        """ Prints text with color for instructions. """
        p = self.point
        self.colored_print(f"{p['fB']}{msg}")

    def process(self, msg: str) -> None:
        """ Prints text with color for processes. """
        p = self.point
        self.colored_print(f"{p['fM']}{msg}")

    def title(self, msg: str) -> None:
        """ Prints text with color for the title. """
        p = self.point
        self.colored_print(f"{p['fC']}{msg}")

    def information(self, msg: str) -> None:
        """ Prints text with color for information. """
        p = self.point
        self.colored_print(f"{p['fW']}{msg}")


class Actions():
    """ Simple actions that changes how the user interacts with the terminal. """
    def clr_scr(self):
        """ Clears the terminal. """
        system = os.name

        os.system('cls' if system == 'nt' else 'clear')


class Objects():
    """ Simple objects which can be displayed onto the terminal. """

    def __init__(self) -> None:
        self.a = Actions()
        self.c = Colors()
    
    def header(self, title: str | None = None, size: int = HEADER_SIZE, newlines: bool = True, clr_scr: bool = True) -> None:
        """ Prints a clean header to the terminal.
        
        ## Params: 
            `title (str | None) = None`: Includes a title in the middle of the header. If set to `None`, there will be just a header. 
            `size (int) = HEADER_SIZE`: How long the header stretches. Optional parameter, defaults to either the terminal size, or the variable `DEFAULT_HEADER_SIZE`.
            `newlines (bool) = True`: If `True` then an empty line will be added before & after the header.
            `clr_scr (bool) = True`: If `True`, will clear the terminal screen, then print the header. """
        
        if clr_scr:
            self.a.clr_scr()
        
        nl = ''
        if newlines:
            nl = '\n'
        
        if title is None:
            self.c.title(f"{nl}{'='*HEADER_SIZE}{nl}")
            return
        
        title = f" {title} "
        self.c.title(f"{nl}{title:=^{size}}{nl}")