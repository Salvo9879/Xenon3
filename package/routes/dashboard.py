
# Import external modules
from flask import Blueprint, render_template
from flask_login import login_required

dashboard_r = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# Routes (dashboard)
@dashboard_r.route('/')
@login_required
def index():
    __title__ = 'Dashboard'
    return render_template('templates/pages/dashboard/index.html', t=__title__)