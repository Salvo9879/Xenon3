
# Import internal modules
from package.exceptions import ApplicationUnavailable, ApplicationNotInstalled
from package.databases import db, Applications
from package.routes import applications_r

import package.package_handler as ph

# Import external modules
from git.repo import Repo

import requests
import os
import git
import importlib

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
    
    def is_application_installed(self, app_uuid: str) -> bool:
        """ Checks whether an application is installed on the Xenon system. """

        abs_path = os.path.abspath(f"package/applications/{app_uuid}")
        return os.path.exists(abs_path)
    
    def get_application_abs_path(self, app_uuid: str) -> str:
        """ Returns the absolute path of the application. """
        return os.path.abspath(f"package/applications/{app_uuid}")
    
    def get_application_url(self, app_uuid: str) -> str:
        """ Gets the application url to it's github repo. """
        if not self.is_application_available(app_uuid):
            raise ApplicationUnavailable(app_uuid)
        
        aa = self.get_available_applications()
        return aa[app_uuid]
    
    def get_application_data(self, app_uuid: str) -> dict:
        """ Gets the applications metadata hardcoded in its `main.py` file. """
        if not self.is_application_installed(app_uuid):
            raise ApplicationNotInstalled(app_uuid)
        
        path = f"package.applications.{app_uuid}.main"
        a = importlib.import_module(path)
        
        md = {
            'uuid': a.UUID,
            'name': a.NAME,
            'description': a.DESCRIPTION,
            'version': a.VERSION,
            'developers': a.DEVELOPERS,
            'icon_path': a.ICON_PATH
        }

        return md

    def add_application_to_db(self, app_uuid: str) -> None:
        """ Adds the application to the database. """
        ad = self.get_application_data(app_uuid)
        
        a = Applications()
        a.uuid = ad['uuid']
        a.name = ad['name']
        a.description = ad['description']
        a.version = ad['version']
        a.developers = ad['developers']
        a.icon_path = ad['icon_path']

        db.session.add(a)
        db.session.commit()

    def remove_application_from_db(self, app_uuid: str) -> None:
        """ Removes an applications row in the database. """
        a = Applications.query.filter_by(uuid=app_uuid).first()
        print(a)

        if a is None:
            return
        
        db.session.delete(a)
        db.session.commit()

    def download_application(self, app_uuid: str) -> None:
        """ Downloads an an available application from a referenced github repo. """
        if not self.is_application_available(app_uuid):
            raise ApplicationUnavailable(app_uuid)
        
        a_url = self.get_application_url(app_uuid)
        ap = self.get_application_abs_path(app_uuid)
        Repo.clone_from(a_url, ap)

        self.add_application_to_db(app_uuid)

    def delete_application(self, app_uuid: str) -> None:
        """ Completely deletes an application off the Xenon system. """
        ap = self.get_application_abs_path(app_uuid)

        git.rmtree(ap)

        self.remove_application_from_db(app_uuid)

    def get_installed_applications(self) -> list:
        """ Returns a list of applications in a `package.applications_handler.Application` instance installed on the Xenon system. """
        abs_path = os.path.abspath('package/applications')

        ia = []
        for app_uuid in os.listdir(abs_path):
            ad = self.get_application_data(app_uuid)
            ia.append(Application(ad))

        return ia

    def register_applications_routes(self) -> None:
        """ Registers all the routes for all the applications. """
        ia = self.get_installed_applications()

        for a in ia:
            a.register_application_routes()

class Application():
    def __init__(self, md: dict) -> None:
        self.uuid = md['uuid']
        self.name = md['name']
        self.description = md['description']
        self.version = md['version']
        self.developers = md['developers']
        self.icon_path = md['icon_path']

        app_path = f"package.applications.{self.uuid}.main"
        self.app_module = importlib.import_module(app_path)
        self.blueprint = self.app_module.blueprint
        
        self.md = md   

    def register_application_routes(self) -> None:
        """ Registers the applications routes to the base application route. """
        applications_r.register_blueprint(self.blueprint)