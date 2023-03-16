
# Import internal modules
from package import ServerSettings, Setup

# Import external modules
from flask import Flask

# Variables
app = Flask(__name__)
ss = ServerSettings()
su = Setup(app, ss)

# Initialization
ss.init()

if __name__ == '__main__':
    su.run()
    if su.ready:
        app.run(
            host=ss.host,
            port=ss.port, 
            debug=ss.debug
        )