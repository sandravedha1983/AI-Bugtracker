from app import create_app
from extensions import db
from models.user import User
from models.bug import Bug

def verify():
    app = create_app()
    with app.app_context():
        try:
            db.create_all()
            print("Database creation success")
            print(f"User count: {User.query.count()}")
            print(f"Bug count: {Bug.query.count()}")
        except Exception as e:
            print(f"Error during verification: {e}")

if __name__ == "__main__":
    verify()
