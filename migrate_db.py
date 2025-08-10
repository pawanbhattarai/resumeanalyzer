
from app import create_app
from models import db, SavedResume

app = create_app()

with app.app_context():
    # Create the saved_resumes table
    db.create_all()
    print("Database migration completed successfully!")
    print("New 'saved_resumes' table created.")
