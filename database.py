# Database initialization module
# This file is used to initialize the database and create tables
# It imports db from models.py to avoid circular imports

from models import db

def init_db(app):
    """Initialize database and create all tables."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    init_db(app)

