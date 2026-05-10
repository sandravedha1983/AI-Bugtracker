from app.extensions import db
from app.models import Bug, User
from sqlalchemy import func
from datetime import datetime, timedelta

def get_priority_distribution():
    """Returns counts of bugs grouped by priority."""
    results = db.session.query(Bug.priority, func.count(Bug.id)).group_by(Bug.priority).all()
    return {priority: count for priority, count in results}

def get_status_overview():
    """Returns counts of bugs grouped by status."""
    results = db.session.query(Bug.status, func.count(Bug.id)).group_by(Bug.status).all()
    return {status: count for status, count in results}

def get_trends_data():
    """Returns number of bugs reported per day for the last 7 days."""
    today = datetime.utcnow().date()
    last_week = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    results = db.session.query(
        func.date(Bug.created_at), 
        func.count(Bug.id)
    ).filter(Bug.created_at >= datetime.utcnow() - timedelta(days=7)).group_by(func.date(Bug.created_at)).all()
    
    counts_map = {str(date): count for date, count in results}
    
    labels = [date.strftime('%a') for date in last_week]
    data = [counts_map.get(str(date), 0) for date in last_week]
    
    return {"labels": labels, "data": data}

def get_developer_load():
    """Returns number of bugs assigned to each developer."""
    results = db.session.query(
        User.name, 
        func.count(Bug.id)
    ).join(Bug, User.id == Bug.assigned_to).filter(User.role == 'developer').group_by(User.name).all()
    
    labels = [r[0] for r in results]
    data = [r[1] for r in results]
    
    return {"labels": labels, "data": data}
def get_severity_distribution():
    """Returns counts of bugs grouped by severity."""
    results = db.session.query(Bug.severity, func.count(Bug.id)).group_by(Bug.severity).all()
    return {severity if severity else "Unassigned": count for severity, count in results}

def get_module_distribution():
    """Returns counts of bugs grouped by module."""
    results = db.session.query(Bug.module, func.count(Bug.id)).group_by(Bug.module).all()
    return {module if module else "Unassigned": count for module, count in results}

def get_ai_accuracy_stats():
    """Mock stats for AI classification (in a real app, this would compare AI vs Human)."""
    return {"accuracy": 85, "precision": 82, "recall": 88}

def get_resolution_trends():
    """Returns average resolution time in hours for the last 7 days."""
    today = datetime.utcnow().date()
    last_week = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    # Generic approach that works for most DBs
    bugs = Bug.query.filter(
        Bug.status == 'Resolved',
        Bug.resolved_at >= datetime.utcnow() - timedelta(days=7)
    ).all()
    
    daily_res = {}
    for bug in bugs:
        date_str = str(bug.resolved_at.date())
        duration = (bug.resolved_at - bug.created_at).total_seconds() / 3600
        if date_str not in daily_res:
            daily_res[date_str] = []
        daily_res[date_str].append(duration)
    
    res_map = {date: round(sum(vals)/len(vals), 1) for date, vals in daily_res.items()}
    
    labels = [date.strftime('%Y-%m-%d') for date in last_week]
    data = [res_map.get(str(date), 0) for date in last_week]
    
    return {"labels": labels, "data": data}
