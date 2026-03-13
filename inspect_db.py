from app import create_app
from extensions import db
from sqlalchemy import inspect, text

def inspect_db():
    app = create_app()
    with app.app_context():
        inspector = inspect(db.engine)
        for table_name in inspector.get_table_names():
            print(f"Table: {table_name}")
            for column in inspector.get_columns(table_name):
                print(f"  Column: {column['name']} ({column['type']})")
        
        # Also try to specifically check the bug table columns
        try:
            res = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bug'"))
            cols = [r[0] for r in res]
            print(f"information_schema columns for 'bug': {cols}")
        except Exception as e:
            print(f"Error querying information_schema: {e}")

if __name__ == "__main__":
    inspect_db()
