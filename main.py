
# Import internal modules
from package.setup import Setup

# Variables
setup = Setup()

if __name__ == '__main__':
    setup.run()  

    if setup.ss:
        from package.server import app, settings

        app.run(
            host=settings.host,
            port=settings.port,
            debug=settings.debug
        )