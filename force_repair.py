from app import create_app
from extensions import db
from models.user import User
from sqlalchemy import text

def force_repair():
    app = create_app()
    with app.app_context():
        print("Starting FORCE repair...")
        
        # 1. Add missing columns using raw connection
        with db.engine.connect() as conn:
            try:
                print("Adding updated_at...")
                conn.execute(text('ALTER TABLE bug ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'))
                conn.commit()
                print("Added updated_at.")
            except Exception as e:
                print(f"Skipping updated_at (might exist or error): {e}")

            try:
                print("Adding resolved_at...")
                conn.execute(text('ALTER TABLE bug ADD COLUMN resolved_at TIMESTAMP'))
                conn.commit()
                print("Added resolved_at.")
            except Exception as e:
                print(f"Skipping resolved_at (might exist or error): {e}")

        # 2. Sanitize ALL admin passwords to avoid "Invalid salt"
        print("Sanitizing admin passwords...")
        admins = User.query.filter_by(role='admin').all()
        for admin in admins:
            print(f"Sanitizing admin: {admin.email}")
            admin.set_password('admin123')
        
        db.session.commit()
        print(f"Sanitized {len(admins)} admin accounts.")

        # 3. Final verification of columns
        with db.engine.connect() as conn:
            res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bug'"))
            cols = [r[0] for r in res]
            print(f"Final column list for 'bug': {cols}")

if __name__ == "__main__":
    force_repair()
