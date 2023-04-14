
# Import external modules
import json

# Variables
PACKAGE_FILE_LOCATION = 'package.json'

def _get_package_file() -> dict:
    """ Gets the content in the `package.json` file. """
    fp = PACKAGE_FILE_LOCATION
    with open(fp, 'r') as f:
        data = json.load(f)
    
    return data

def _modify_package_file(attr: str, v: any) -> None:
    """ Modifies an attribute value in the `package.json` file by replacing it with `v`. """
    pf = _get_package_file()
    pf[attr] = v

    fp = PACKAGE_FILE_LOCATION
    with open(fp, 'w') as f:
        json.dump(pf, f, indent=4) # TODO: Change indent to make the file smaller.

# Get
def get_app_settings_path() -> str:
    """ Gets the `app-settings-path` from the `package.json` file. """
    return _get_package_file()['app-settings-path']

def get_file_url() -> str:
    """ Gets the `get-file-url` from the `package.json` file. """
    return _get_package_file()['get-file-url']

def get_db_paths() -> dict:
    """ Gets the `db-paths` from the `package.json` file. """
    db_uris = _get_package_file()['db-paths']
    return db_uris

# Set
def set_db_paths(v: any) -> None:
    """ Sets the `db-paths` in the `package.json`. """
    _modify_package_file('db-paths', v)

def get_available_apps_url() -> str:
    """ Gets the `available-application-url` from the `package.json` file. """
    return _get_package_file()['available-application-url']