""" 
Categories:
    - System > Operating system > Python download > Dependencies
    - Storage
    - Hardware
    - Internet
    - Server 
    - Customization
    - Security
    - Logs
    - Activity
    - User settings
    - Notifications
    - Statistics
    - Support
    - Focuses
"""

# Import external modules
from flask import Blueprint, render_template, redirect, url_for

# Blueprint declaration
settings_r = Blueprint('settings', __name__, url_prefix='/settings')

# Routes
@settings_r.route('/index')
def index():
    # TODO: Create a settings index page.
    return redirect(url_for('pages.settings.system'))

@settings_r.route('/system')
def system():
    __title__ = 'System'
    return render_template('templates/pages/settings/system.html', t=__title__)

@settings_r.route('/storage')
def storage():
    __title__ = 'Storage'
    return render_template('templates/pages/settings/storage.html', t=__title__)

@settings_r.route('/hardware')
def hardware():
    __title__ = 'Hardware'
    return render_template('templates/pages/settings/hardware.html', t=__title__)

@settings_r.route('/internet')
def internet():
    __title__ = 'Internet'
    return render_template('templates/pages/settings/internet.html', t=__title__)

@settings_r.route('/server')
def server():
    __title__ = 'Server'
    return render_template('templates/pages/settings/server.html', t=__title__)

@settings_r.route('/customization')
def customization():
    __title__ = 'Customization'
    return render_template('templates/pages/settings/customization.html', t=__title__)

@settings_r.route('/security')
def security():
    __title__ = 'Security'
    return render_template('templates/pages/settings/security.html', t=__title__)

@settings_r.route('/logs')
def logs():
    __title__ = 'Logs'
    return render_template('templates/pages/settings/logs.html', t=__title__)

@settings_r.route('/activity')
def activity():
    __title__ = 'Activity'
    return render_template('templates/pages/settings/activity.html', t=__title__)

@settings_r.route('/profile_settings')
def profile_settings():
    __title__ = 'Profile Settings'
    return render_template('templates/pages/settings/profile_settings.html', t=__title__)

@settings_r.route('/notifications')
def notifications():
    __title__ = 'Notifications'
    return render_template('templates/pages/settings/notifications.html', t=__title__)

@settings_r.route('/statistics')
def statistics():
    __title__ = 'Statistics'
    return render_template('templates/pages/settings/statistics.html', t=__title__)

@settings_r.route('/support')
def support():
    __title__ = 'Support'
    return render_template('templates/pages/settings/support.html', t=__title__)

