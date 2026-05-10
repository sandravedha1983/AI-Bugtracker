import logging
from datetime import datetime
from app.extensions import db
from app.models import Bug, AuditLog
from app.services.ai_service import predict_priority, generate_summary
from app.services.github_service import create_github_issue

logger = logging.getLogger(__name__)

class BugService:
    @staticmethod
    def create_bug(title, description, reporter_id):
        try:
            # AI Classification
            try:
                priority = predict_priority(description)
                ai_summary = generate_summary(description)
            except Exception as e:
                logger.error(f"AI Service error: {e}")
                priority = "Medium"
                ai_summary = description[:100]

            # GitHub Integration
            from app.services.github_service import GitHubService
            gh_service = GitHubService()
            github_url, github_issue_number = gh_service.create_issue(title, description)

            new_bug = Bug(
                title=title,
                description=description,
                priority=priority,
                ai_summary=ai_summary,
                created_by=reporter_id,
                github_url=github_url,
                github_issue_number=github_issue_number
            )
            
            db.session.add(new_bug)
            db.session.commit()

            AuditLog.log(
                action="CREATE_BUG",
                user_id=reporter_id,
                target_type="Bug",
                target_id=new_bug.id,
                details=f"Bug created with priority {priority}"
            )

            return new_bug
        except Exception as e:
            logger.error(f"Failed to create bug: {e}")
            db.session.rollback()
            raise

    @staticmethod
    def update_status(bug_id, status, user_id):
        bug = Bug.query.get_or_404(bug_id)
        old_status = bug.status
        
        bug.status = status
        if status == 'Resolved':
            bug.resolved_at = datetime.utcnow()
        else:
            bug.resolved_at = None
        
        # Sync with GitHub
        if bug.github_issue_number:
            from app.services.github_service import GitHubService
            gh_service = GitHubService()
            gh_service.update_issue_status(bug.github_issue_number, status)

        db.session.commit()

        AuditLog.log(
            action="UPDATE_BUG_STATUS",
            user_id=user_id,
            target_type="Bug",
            target_id=bug.id,
            details=f"Status changed from {old_status} to {status}"
        )
        
        return bug

    @staticmethod
    def assign_bug(bug_id, developer_id, assigner_id):
        bug = Bug.query.get_or_404(bug_id)
        bug.assigned_to = developer_id
        db.session.commit()

        AuditLog.log(
            action="ASSIGN_BUG",
            user_id=assigner_id,
            target_type="Bug",
            target_id=bug.id,
            details=f"Assigned to user ID {developer_id}"
        )
        
        return bug

    @staticmethod
    def soft_delete(bug_id, user_id):
        bug = Bug.query.get_or_404(bug_id)
        bug.is_deleted = True
        bug.deleted_at = datetime.utcnow()
        db.session.commit()

        AuditLog.log(
            action="DELETE_BUG",
            user_id=user_id,
            target_type="Bug",
            target_id=bug.id,
            details="Soft deleted bug"
        )
        
        return True
