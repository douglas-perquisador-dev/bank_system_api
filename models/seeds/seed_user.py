from config import db
from models.users import User
from config import app

@app.cli.command("seed_user")
def seed_user():
    """Seed the database with initial data."""
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='123456')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
