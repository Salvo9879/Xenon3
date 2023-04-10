
# Import external modules
import os
import json

class Application():
    """ A instance of a application which exists in Xenon. """
    def __init__(self, md: dict) -> None:
        self.md = md

        self.app_uuid = md['app-uuid']
        self.name = md['name']
        self.description = md['description']
        self.version = md['version']
        self.icon_url = md['icon-url']
        self.developers = md['developers']

class ApplicationManager():
    """ Manages all the applications in Xenon. """
    def __init__(self) -> None:
        self.abs_path = self.get_application_abs_path()

    @property
    def installed_applications(self) -> list:
        return self.get_installed_applications()

    def get_installed_applications(self) -> list:
        """ Returns a list of uuids of all installed applications in Xenon. """
        return os.listdir(self.abs_path)
    
    def get_application_abs_path(self, app_uuid: str | None = None) -> str:
        if app_uuid is None:
            app_uuid = ''

        return os.path.abspath(f"package/applications/{app_uuid}")
    
    def get_application_content(self, app_uuid: str) -> dict:
        """ Gets the content from the applications `manifest.json` file. """
        abs_path = self.get_application_abs_path(app_uuid)
        m_fp = os.path.abspath(f"{abs_path}/manifest.json")

        with open(m_fp, 'r') as f:
            data = json.load(f)

        return data
    
    def application_exist(self, app_uuid) -> bool:
        """ Tests whether an application with a given uuid exists in Xenon. """
        return app_uuid in self.installed_applications
    
    def get_application(self, app_uuid: str) -> Application | None:
        """ Gets an application based on a uuid. Returns `None` if the application is not found; else the application instance is returned. """
        if not self.application_exist(app_uuid):
            return None
        
        content_data = self.get_application_content(app_uuid)
        return Application(content_data)