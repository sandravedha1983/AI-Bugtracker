from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from extensions import db

from models import Bug, User
from utils.analytics_utils import (
    get_priority_distribution, 
    get_status_overview, 
    get_trends_data, 
    get_developer_load,
    get_resolution_trends
)


api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/analytics/priority', methods=['GET'])
@login_required
def priority_dist():
    return jsonify(get_priority_distribution())


@api_bp.route('/bugs', methods=['GET'])
@login_required
def get_bugs():
    """
    Get All Bugs
    ---
    tags:
      - Bug Management
    responses:
      200:
        description: A list of bugs
    """
    bugs = Bug.query.all()
    return jsonify([bug.to_dict() for bug in bugs])

@api_bp.route('/bugs', methods=['POST'])
@login_required
def add_bug():
    """
    Create a New Bug
    ---
    tags:
      - Bug Management
    responses:
      201:
        description: Bug created successfully
    """
    # Placeholder for actual implementation in Feature 4
    return jsonify({"message": "Bug created successfully"}), 201

@api_bp.route('/bugs/<int:bug_id>', methods=['PUT'])
@login_required
def update_bug(bug_id):
    """
    Update Bug Status
    ---
    tags:
      - Bug Management
    responses:
      200:
        description: Bug status updated successfully
    """
    bug = Bug.query.get_or_404(bug_id)
    if current_user.role == 'developer' and bug.assigned_to != current_user.id:
        return jsonify({"message": "Permission denied"}), 403
    
    new_status = request.form.get('status')
    if new_status:
        bug.status = new_status
        db.session.commit()
        return jsonify({"message": f"Status updated to {new_status}"}), 200
    return jsonify({"message": "No status provided"}), 400

@api_bp.route('/analytics/status', methods=['GET'])
@login_required
def status_distribution():
    """
    Bug Status Overview
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Count of bugs per status
    """
    return jsonify(get_status_overview())

@api_bp.route('/analytics/trends', methods=['GET'])
@login_required
def trends():
    """
    Bugs Reported Over Time
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Daily bug counts for the last 7 days
    """
    return jsonify(get_trends_data())

@api_bp.route('/analytics/developer-load', methods=['GET'])
@login_required
def developer_load():
    """
    Developer Workload
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Number of assigned bugs per developer
    """
    return jsonify(get_developer_load())


@api_bp.route('/analytics/resolution-trend', methods=['GET'])
@login_required
def resolution_trend():
    """
    Resolution time trend
    ---
    tags:
      - Analytics
    responses:
      200:
        description: Average resolution time in hours
    """
    return jsonify(get_resolution_trends())

