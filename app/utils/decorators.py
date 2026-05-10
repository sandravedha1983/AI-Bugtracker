from functools import wraps
from flask import flash, redirect, url_for, request, jsonify
from flask_login import current_user

def role_required(roles):
    """Decorator to restrict access to specific user roles."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if request.path.startswith('/api/'):
                    return jsonify(error="Unauthorized", message="Authentication required"), 401
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('main.login'))
            
            if current_user.role not in roles:
                if request.path.startswith('/api/'):
                    return jsonify(error="Forbidden", message="Insufficient permissions"), 403
                flash('You do not have permission to perform this action.', 'danger')
                return redirect(url_for('main.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return role_required(['admin'])(f)

def lead_required(f):
    return role_required(['admin', 'lead'])(f)

def developer_required(f):
    return role_required(['admin', 'lead', 'developer'])(f)

def tester_required(f):
    return role_required(['admin', 'lead', 'developer', 'tester'])(f)
