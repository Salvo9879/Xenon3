
# Import internal modules
from package import ServerSettings, Setup, db

# Import external modules
from flask import Flask

# Variables
app = Flask(__name__)
ss = ServerSettings(app)
su = Setup(ss)

# Initialization
ss.init()
db.init_app(app)

if __name__ == '__main__':
    su.run()
    if su.ready:
        app.run(
            host=ss.host,
            port=ss.port, 
            debug=ss.debug
        )