import os
import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from models import User, Bug
from services.ai_service import predict_priority, generate_summary
from utils.email_utils import send_verification_email
from utils.decorators import role_required, admin_required, developer_required, tester_required
from flask_dance.contrib.google import google
from services.github_service import create_github_issue

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('home.html')

@main_bp.before_app_request
def update_last_active():
    if current_user.is_authenticated:
        current_user.last_active_at = datetime.utcnow()
        db.session.commit()

from extensions import limiter, db


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        
        print(f"Login attempt for: '{email}'")
        
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                print(f"User not found in DB: '{email}'")
            
            if user and user.check_password(password):
                if user.is_suspended:
                    flash('Your account has been suspended. Please contact support.', 'danger')
                    return redirect(url_for('main.login'))
                if not user.is_verified:
                    flash('Please verify your email before logging in.', 'warning')
                    return redirect(url_for('main.login'))
                
                login_user(user)
                return redirect(url_for('main.dashboard'))
            else:
                flash("Invalid credentials", 'danger')
                return redirect(url_for('main.login'))
        except Exception as e:
            print("Auth error:", e)
            flash('Something went wrong', 'danger')
            return redirect(url_for('main.login'))
            
    return render_template('login.html')

@main_bp.route('/signup', methods=['GET', 'POST'])

def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        role = request.form.get('role', 'tester')

        print(f"Signup attempt for: '{email}'")

        try:
            email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
            if not re.match(email_regex, email):
                flash('Invalid email format.', 'danger')
                return redirect(url_for('main.signup'))
            
            if len(password) < 6:
                flash('Password must be at least 6 characters.', 'danger')
                return redirect(url_for('main.signup'))

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("User already exists", 'danger')
                return redirect(url_for('main.signup'))

            new_user = User(name=name, email=email, role=role, is_verified=False)
            new_user.set_password(password)
            
            from utils.email_utils import generate_otp
            otp = generate_otp()
            new_user.verification_code = otp
            from datetime import datetime, timedelta
            new_user.verification_expiry = datetime.utcnow() + timedelta(hours=1)
            
            db.session.add(new_user)
            db.session.commit()
            
            if send_verification_email(email, otp):
                flash('Signup successful! Please check your email for the 6-digit verification code.', 'success')
                return redirect(url_for('main.verify_otp', email=email))
            else:
                flash('Signup successful, but the verification email could not be sent. Please contact support.', 'warning')
                return redirect(url_for('main.login'))
        except Exception as e:
            print("Auth error:", e)
            flash("Something went wrong", "danger")
            return redirect(url_for("main.signup"))

    return render_template('signup.html')

@main_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    email = request.args.get('email', '').strip().lower()
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        otp = request.form.get('otp')
        
        print(f"OTP Verification attempt for: '{email}' with code: {otp}")
        
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"User not found for OTP: '{email}'")
            flash('User not found.', 'danger')
            return redirect(url_for('main.signup'))
        
        if user.is_verified:
            flash('Account already verified. Please login.', 'info')
            return redirect(url_for('main.login'))
            
        if user.verification_code == otp:
            from datetime import datetime
            if user.verification_expiry and user.verification_expiry > datetime.utcnow():
                user.is_verified = True
                user.verification_code = None
                user.verification_expiry = None
                db.session.commit()
                flash('Your account has been verified! You can now login.', 'success')
                return redirect(url_for('main.login'))
            else:
                flash('Verification code has expired. Please request a new one.', 'danger')
        else:
            flash('Invalid verification code.', 'danger')
            
    return render_template('verify_otp.html', email=email)

@main_bp.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification_request():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        print(f"Resend verification requested for: '{email}'")
        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_verified:
                flash('Your account is already verified.', 'info')
            else:
                from utils.email_utils import generate_otp
                otp = generate_otp()
                user.verification_code = otp
                from datetime import datetime, timedelta
                user.verification_expiry = datetime.utcnow() + timedelta(hours=1)
                db.session.commit()
                
                if send_verification_email(email, otp):
                    flash('A new verification code has been sent.', 'success')
                    return redirect(url_for('main.verify_otp', email=email))
                else:
                    flash('Failed to send verification email. Please try again later.', 'danger')
        else:
            flash('Email not found.', 'danger')
        return redirect(url_for('main.login'))
    return render_template('resend_verification.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route("/login/google/authorized")
def google_authorized():
    try:
        if not google.authorized:
            return redirect(url_for("google.login"))

        resp = google.get("/oauth2/v2/userinfo")
        if not resp.ok:
            return "Google login failed", 400

        user_info = resp.json()
        email = user_info.get("email")

        if not email:
            return "Email not found", 400

        name = user_info.get("name", email.split('@')[0])

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                name=name,
                email=email,
                role="tester",
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        flash(f"Successfully signed in as {name}", "success")
        return redirect(url_for("main.dashboard"))
    except Exception as e:
        print("Google OAuth error:", e)
        return "OAuth failed", 500

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Generic dashboard redirector based on role."""
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
    elif current_user.role == 'lead':
        return redirect(url_for('main.lead_dashboard'))
    elif current_user.role == 'developer':
        return redirect(url_for('main.developer_dashboard'))
    else: # tester
        return redirect(url_for('main.tester_dashboard'))

@main_bp.route('/admin/dashboard')
@login_required
@role_required(['admin'])
def admin_dashboard():
    stats = {
        'total_bugs': Bug.query.count(),
        'open_bugs': Bug.query.filter_by(status='Open').count(),
        'unassigned_bugs': Bug.query.filter_by(assigned_to=None).count(),
        'total_users': User.query.count()
    }
    recent_bugs = Bug.query.order_by(Bug.created_at.desc()).limit(10).all()
    return render_template('dashboards/admin.html', stats=stats, recent_bugs=recent_bugs)

@main_bp.route('/lead/dashboard')
@login_required
@role_required(['lead'])
def lead_dashboard():
    stats = {
        'total_bugs': Bug.query.count(),
        'open_bugs': Bug.query.filter_by(status='Open').count(),
        'unassigned_bugs': Bug.query.filter_by(assigned_to=None).count()
    }
    recent_bugs = Bug.query.order_by(Bug.created_at.desc()).limit(10).all()
    return render_template('dashboards/lead.html', stats=stats, recent_bugs=recent_bugs)

@main_bp.route('/developer/dashboard')
@login_required
@role_required(['developer'])
def developer_dashboard():
    stats = {
        'assigned_bugs': Bug.query.filter_by(assigned_to=current_user.id).count(),
        'in_progress': Bug.query.filter_by(assigned_to=current_user.id, status='In Progress').count(),
        'resolved': Bug.query.filter_by(assigned_to=current_user.id, status='Resolved').count()
    }
    bugs = Bug.query.filter_by(assigned_to=current_user.id).order_by(Bug.created_at.desc()).all()
    return render_template('dashboards/developer.html', stats=stats, bugs=bugs)

@main_bp.route('/tester/dashboard')
@login_required
@role_required(['tester'])
def tester_dashboard():
    stats = {
        'reported_bugs': Bug.query.filter_by(created_by=current_user.id).count(),
        'open_bugs': Bug.query.filter_by(created_by=current_user.id, status='Open').count(),
        'resolved_bugs': Bug.query.filter_by(created_by=current_user.id, status='Resolved').count()
    }
    bugs = Bug.query.filter_by(created_by=current_user.id).order_by(Bug.created_at.desc()).all()
    return render_template('dashboards/tester.html', stats=stats, bugs=bugs)


@main_bp.route('/bugs')
@login_required
def bugs():
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    search_query = request.args.get('search')
    
    query = Bug.query
    
    if current_user.role == 'developer':
        query = query.filter_by(assigned_to=current_user.id)
    elif current_user.role == 'tester':
        query = query.filter_by(created_by=current_user.id)
        
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    if search_query:
        query = query.filter(Bug.title.contains(search_query) | Bug.description.contains(search_query))
        
    bugs_list = query.order_by(Bug.created_at.desc()).all()
    developers = User.query.filter_by(role='developer').all()
    
    return render_template('bugs.html', bugs=bugs_list, developers=developers)

@main_bp.route('/bug/add', methods=['POST'])
@login_required
@tester_required
def add_bug():
    title = request.form.get('title')
    description = request.form.get('description')
    
    try:
        priority = predict_priority(description)
        ai_summary = generate_summary(description)
    except Exception as e:
        print(f"AI Error: {e}")
        priority = "Medium"
        ai_summary = description[:100]

    # Create GitHub Issue
    github_url = create_github_issue(title, description)

    new_bug = Bug(
        title=title,
        description=description,
        priority=priority,
        ai_summary=ai_summary,
        created_by=current_user.id,
        github_url=github_url
    )
    
    db.session.add(new_bug)
    db.session.commit()
    
    flash(f'Bug reported successfully! AI suggested priority: {priority}', 'success')
    if github_url:
        flash(f'GitHub issue created: <a href="{github_url}" target="_blank">{github_url}</a>', 'info')
    
    return redirect(url_for('main.bugs'))

@main_bp.route('/bug/assign/<int:bug_id>', methods=['POST'])
@login_required
@role_required(['admin', 'lead'])
def assign_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    dev_id = request.form.get('developer_id')
    bug.assigned_to = dev_id
    db.session.commit()
    flash('Bug assigned successfully', 'success')
    return redirect(url_for('main.bugs'))

@main_bp.route('/bug/status/<int:bug_id>', methods=['POST'])
@login_required
def update_status(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    
    if current_user.role == 'developer' and bug.assigned_to != current_user.id:
        flash('Permission denied', 'danger')
        return redirect(url_for('main.bugs'))
    
    new_status = request.form.get('status')
    if new_status == 'Resolved' and bug.status != 'Resolved':
        bug.resolved_at = datetime.utcnow()
    elif new_status != 'Resolved':
        bug.resolved_at = None
        
    bug.status = new_status
    db.session.commit()

    flash(f'Status updated to {new_status}', 'success')
    return redirect(url_for('main.bugs'))

@main_bp.route('/bug/delete/<int:bug_id>', methods=['POST'])
@login_required
@admin_required
def delete_bug(bug_id):
    bug = Bug.query.get_or_404(bug_id)
    db.session.delete(bug)
    db.session.commit()
    flash('Bug deleted', 'info')
    return redirect(url_for('main.bugs'))
