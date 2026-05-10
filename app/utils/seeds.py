import os
from app.extensions import db
from app.models import User, Bug
from datetime import datetime

def seed_database(app):
    with app.app_context():
        # Seed default admin if missing
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@bugtracker.com')
        admin_user = User.query.filter_by(email=admin_email).first()
        if not admin_user:
            app.logger.info(f"Seeding default admin user: {admin_email}")
            new_admin = User(
                name="System Admin",
                email=admin_email,
                role="admin",
                is_verified=True
            )
            admin_pass = os.environ.get('ADMIN_PASSWORD', 'admin123')
            new_admin.set_password(admin_pass)
            db.session.add(new_admin)
            db.session.commit()
            app.logger.info("Admin user created successfully.")

        # Optional: Seed some sample data for analytics if in development
        if app.config.get('DEBUG') and Bug.query.count() == 0:
            app.logger.info("Seeding sample bug data...")
            # Add some sample bugs here if needed
            pass
