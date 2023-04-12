
# Import internal modules
from package.exceptions import ApplicationUnavailable

import package.package_handler as ph

# Import external modules
from git.repo import Repo

import requests
import os
import git

# TODO: Create barrier which prevents applications being downloaded or deleted without ADMIN authentication.

class ApplicationManager():
    """ Used to download/delete/manage applications on a large scale. """
    def get_available_applications(self) -> dict:
        """ Gets a dictionary of Xenon applications. The key refers to the app uuid & the value refers to the git repo url. """
        aa_url = ph.get_available_apps_url()

        r = requests.get(aa_url)
        return r.json()

    def is_application_available(self, app_uuid: str) -> bool:
        """ Checks whether a given app uuid is referenced as available. """
        aa = self.get_available_applications()

        return app_uuid in aa
    
    def get_application_abs_path(self, app_uuid: str) -> str:
        """ Returns the absolute path of the application. """
        return os.path.abspath(f"package/applications/{app_uuid}")
    
    def get_application_url(self, app_uuid: str) -> str:
        """ Gets the application url to it's github repo. """
        if not self.is_application_available(app_uuid):
            raise ApplicationUnavailable(app_uuid)
        
        aa = self.get_available_applications()
        return aa[app_uuid]

    def download_application(self, app_uuid: str) -> None:
        """ Downloads an an available application from a referenced github repo. """
        if not self.is_application_available(app_uuid):
            raise ApplicationUnavailable(app_uuid)
        
        a_url = self.get_application_url(app_uuid)
        ap = self.get_application_abs_path(app_uuid)
        Repo.clone_from(a_url, ap)

    def delete_application(self, app_uuid: str) -> None:
        ap = self.get_application_abs_path(app_uuid)

        git.rmtree(ap)