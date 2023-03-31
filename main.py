
# Import internal modules
from package.setup import Setup

# Variables
su = Setup()
    

if __name__ == '__main__':
    su.run()

    if su.setup_successful:
        from package.server import app

        app.run()