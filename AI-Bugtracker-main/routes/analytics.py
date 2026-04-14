from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from utils.decorators import admin_required
from utils.analytics_utils import (
    get_priority_distribution, 
    get_status_overview, 
    get_trends_data, 
    get_developer_load
)

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
@admin_required
def dashboard():
    return render_template('analytics.html')

