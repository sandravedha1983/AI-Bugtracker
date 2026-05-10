from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session, current_app
from flask_login import current_user, login_required
from app.utils.decorators import admin_required
from app.extensions import db
from app.models import User, Bug, AuditLog
from app.services.bug_service import BugService
from app.utils.email_utils import send_verification_email, generate_otp
from app.utils.analytics_utils import (
    get_priority_distribution, 
    get_status_overview, 
    get_trends_data, 
    get_developer_load
)
from datetime import datetime, timedelta

admin_bp = Blueprint('platform_admin', __name__, url_prefix='/platform-admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("admin_authenticated"):
        return redirect(url_for('platform_admin.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        print("Admin login attempt:", email)
        
        try:
            user = User.query.filter_by(email=email, role='admin').first()
            
            if user and user.check_password(password):
                session["admin_authenticated"] = True
                session["admin_user_id"] = user.id
                flash("Admin session started.", "success")
                return redirect(url_for('platform_admin.dashboard'))
            else:
                flash("Invalid admin credentials", "danger")
        except Exception as e:
            print("Admin Auth Error:", e)
            flash("An error occurred during admin login.", "danger")
            
    return render_template('platform_admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop("admin_authenticated", None)
    flash("Admin session ended.", "info")
    return redirect(url_for('platform_admin.login'))

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    online_threshold = datetime.utcnow() - timedelta(minutes=5)
    stats = {
        'total_users': User.query.count(),
        'unverified_users': User.query.filter_by(is_verified=False).count(),
        'suspended_users': User.query.filter_by(is_suspended=True).count(),
        'online_devs': User.query.filter(User.role == 'developer', User.last_active_at >= online_threshold).count(),
        'total_bugs': Bug.query.count(),
        'unassigned_bugs': Bug.query.filter_by(assigned_to=None).count()
    }
    return render_template('platform_admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users_list = User.query.all()
    now = datetime.utcnow()
    return render_template('platform_admin/users.html', users=users_list, now=now)

@admin_bp.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.email} deleted.", "success")
    return redirect(url_for('platform_admin.users'))

@admin_bp.route('/user/suspend/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_suspend(user_id):
    user = User.query.get_or_404(user_id)
    user.is_suspended = not user.is_suspended
    db.session.commit()
    status = "suspended" if user.is_suspended else "unsuspended"
    flash(f"User {user.email} {status}.", "info")
    return redirect(url_for('platform_admin.users'))

@admin_bp.route('/user/role/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def change_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    if new_role in ['admin', 'lead', 'developer', 'tester']:
        user.role = new_role
        db.session.commit()
        flash(f"Role updated for {user.email}.", "success")
    return redirect(url_for('platform_admin.users'))

@admin_bp.route('/developers')
@login_required
@admin_required
def developers():
    devs = User.query.filter_by(role='developer').all()
    now = datetime.utcnow()
    for dev in devs:
        dev.workload = Bug.query.filter_by(assigned_to=dev.id, status='Open').count()
        dev.current_bug = Bug.query.filter_by(assigned_to=dev.id, status='In Progress').first()
    return render_template('platform_admin/developers.html', devs=devs, now=now)

@admin_bp.route('/bug-assignment')
@login_required
@admin_required
def bug_assignment():
    unassigned_bugs = Bug.query.filter_by(assigned_to=None).all()
    devs = User.query.filter_by(role='developer').all()
    now = datetime.utcnow()
    online_threshold = now - timedelta(minutes=5)
    
    suggestions = {}
    for bug in unassigned_bugs:
        online_devs = [d for d in devs if d.last_active_at >= online_threshold]
        if online_devs:
            suggested = min(online_devs, key=lambda d: Bug.query.filter_by(assigned_to=d.id, status='Open').count())
        else:
            suggested = min(devs, key=lambda d: Bug.query.filter_by(assigned_to=d.id, status='Open').count()) if devs else None
        suggestions[bug.id] = suggested

    return render_template('platform_admin/bug_assignment.html', bugs=unassigned_bugs, devs=devs, suggestions=suggestions, now=now)

@admin_bp.route('/email-management')
@login_required
@admin_required
def email_management():
    users_list = User.query.all()
    return render_template('platform_admin/email_management.html', users=users_list)

@admin_bp.route('/email/verify/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def manual_verify(user_id):
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    flash(f"User {user.email} manually verified.", "success")
    return redirect(url_for('platform_admin.email_management'))

@admin_bp.route('/database')
@login_required
@admin_required
def database():
    target = request.args.get('table', 'users')
    if target == 'bugs':
        data = Bug.query.all()
        cols = ['id', 'title', 'priority', 'status', 'assigned_to']
    else:
        data = User.query.all()
        cols = ['id', 'name', 'email', 'role', 'is_verified']
    return render_template('platform_admin/database.html', data=data, cols=cols, table=target)

@admin_bp.route('/bug/assign/<int:bug_id>', methods=['POST'])
@login_required
@admin_required
def assign_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    dev_id = request.form.get('developer_id')
    bug.assigned_to = dev_id
    db.session.commit()
    flash('Bug assigned successfully', 'success')
    return redirect(request.referrer or url_for('platform_admin.bug_assignment'))
@admin_bp.route('/bug/auto-assign/<int:bug_id>', methods=['POST'])
@login_required
@admin_required
def auto_assign_dev_action(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    devs = User.query.filter_by(role='developer').all()
    if not devs:
        flash("No developers available.", "danger")
        return redirect(url_for('platform_admin.bug_assignment'))
    
    now = datetime.utcnow()
    online_threshold = now - timedelta(minutes=5)
    online_devs = [d for d in devs if d.last_active_at >= online_threshold]
    
    if online_devs:
        suggested = min(online_devs, key=lambda d: Bug.query.filter_by(assigned_to=d.id, status='Open').count())
    else:
        suggested = min(devs, key=lambda d: Bug.query.filter_by(assigned_to=d.id, status='Open').count())
        
    bug.assigned_to = suggested.id
    db.session.commit()
    flash(f"Bug assigned to {suggested.name}", "success")
    return redirect(url_for('platform_admin.bug_assignment'))

@admin_bp.route('/user/resend-verification/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def resend_verification(user_id):
    user = User.query.get_or_404(user_id)
    otp = generate_otp()
    user.verification_code = otp
    user.verification_expiry = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()
    
    if send_verification_email(user.email, otp):
        flash(f"Verification email sent to {user.email}", "success")
    else:
        flash("Failed to send verification email.", "danger")
    return redirect(url_for('platform_admin.email_management'))
@admin_bp.route('/database/delete-bug/<int:bug_id>', methods=['POST'])
@login_required
@admin_required
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    db.session.delete(bug)
    db.session.commit()
    flash("Bug deleted from database.", "info")
    return redirect(url_for('platform_admin.database', table='bugs'))

@admin_bp.route('/api/stats/priority')
@login_required
@admin_required
def api_priority():
    return jsonify(get_priority_distribution())

@admin_bp.route('/api/stats/status')
@login_required
@admin_required
def api_status():
    return jsonify(get_status_overview())

@admin_bp.route('/api/stats/trends')
@login_required
@admin_required
def api_trends():
    return jsonify(get_trends_data())

@admin_bp.route('/api/stats/developer-load')
@login_required
@admin_required
def api_dev_load():
    return jsonify(get_developer_load())
