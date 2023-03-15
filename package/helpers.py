
# Import internal modules
import socket
import json
import requests
import subprocess
import os

def get_all_packages():
    """ Gets all packages installed onto the machine. """
    res = subprocess.run('pip freeze', text=True, capture_output=True)
    return res.stdout.splitlines()

def download_package(pn: str, co: bool = False) -> None:
    """ Downloads a package via pip. """
    subprocess.run(f"pip install {pn}", text=True, capture_output=co)

def is_pip_configured():
    """ Tests whether pip is installed & if it is updated to the latest version. """
    try:
        import pip
        return True
    except ModuleNotFoundError:
        return False
    
def download_pip(co: bool = False):
    """ Downloads & upgrades pip. """
    subprocess.run('python -m pip install --upgrade pip', shell=True, text=True, capture_output=co)


def is_online():
    """ Returns a boolean based on whether the server can actively connect to external networks. """
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
        return True
    except socket.error:
        return False
    
def get_online_resource(fp: str):
    """ Gets the context of a file hosted online. """
    cpf = get_package_file()
    gf_url = cpf['get_file_url']
    t_url = f"{gf_url}/{fp}"

    r = requests.get(t_url)

    try:
        return r.json()
    except ValueError:
        return r.text
    
def get_online_package_file():
    """ Returns the context of the `package.json` file hosted online. This can be used to get the latest version of Xenon. """
    return get_online_resource('package.json')

def get_package_file():
    """ Returns the context of the `package.json` file. Returns error if the file cannot be found. """
    with open('package.json', 'r') as f:
        data = json.load(f)
    return data

def get_system():
    """ Gets the name of the machines operating system. """

    system = os.name
    return system