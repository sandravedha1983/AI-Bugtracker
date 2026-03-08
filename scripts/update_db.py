import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from sqlalchemy import text

def update_schema():
    app = create_app()
    with app.app_context():
        print("Checking database schema updates...")
        try:
            # Check if columns exist
            db.session.execute(text("ALTER TABLE \"user\" ADD COLUMN verification_code VARCHAR(6)"))
            db.session.execute(text("ALTER TABLE \"user\" ADD COLUMN verification_expiry TIMESTAMP"))
            db.session.commit()
            print("Successfully added verification_code and verification_expiry columns.")
        except Exception as e:
            if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                print("Columns already exist. No update needed.")
            else:
                print(f"Error updating schema: {e}")
                print("Tip: If this is a fresh development setup, you can also drop the table and let db.create_all() recreate it.")

if __name__ == "__main__":
    update_schema()
