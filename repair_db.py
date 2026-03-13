import os
from app import create_app
from extensions import db, bcrypt
from models.user import User
from models.bug import Bug
from sqlalchemy import text

def repair():
    app = create_app()
    with app.app_context():
        print("Starting database repair...")
        
        # 1. Add missing columns to Bug table
        try:
            db.session.execute(text('ALTER TABLE bug ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'))
            db.session.execute(text('ALTER TABLE bug ADD COLUMN IF NOT EXISTS resolved_at TIMESTAMP'))
            db.session.commit()
            print("Bug table schema updated.")
        except Exception as e:
            db.session.rollback()
            print(f"Error updating Bug table: {e}")

        # 2. Fix Admin Password (or create one if missing)
        admin_email = "admin@bugtracker.ai" # Default admin email from templates
        admin = User.query.filter_by(role='admin').first()
        
        if admin:
            print(f"Found admin user: {admin.email}. Resetting password to 'admin123' for verification.")
            admin.set_password('admin123')
            db.session.commit()
            print("Admin password reset successfully.")
        else:
            print("No admin user found. Creating default admin: admin@bugtracker.ai / admin123")
            new_admin = User(
                name="System Administrator",
                email=admin_email,
                role="admin",
                is_verified=True
            )
            new_admin.set_password('admin123')
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin created.")

        print("Database repair complete.")

if __name__ == "__main__":
    repair()
