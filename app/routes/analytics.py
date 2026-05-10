from flask import Blueprint, jsonify, render_template
from flask_login import login_required
from app.utils.decorators import lead_required
from app.utils.analytics_utils import (
    get_priority_distribution, 
    get_status_overview, 
    get_trends_data, 
    get_developer_load,
    get_severity_distribution,
    get_module_distribution,
    get_resolution_trends,
    get_ai_accuracy_stats
)

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
@lead_required
def dashboard():
    return render_template('analytics.html')

@analytics_bp.route('/api/analytics/summary')
@login_required
@lead_required
def api_summary():
    return jsonify({
        "priority": get_priority_distribution(),
        "status": get_status_overview(),
        "trends": get_trends_data(),
        "dev_load": get_developer_load(),
        "severity": get_severity_distribution(),
        "module": get_module_distribution(),
        "resolution": get_resolution_trends(),
        "ai_stats": get_ai_accuracy_stats()
    })

