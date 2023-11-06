from models import db, connect_db, User, Code
from app import app, bcrypt

# Create all tables

db.drop_all()
db.create_all()

# If table isn't empty, empty it.

User.query.delete()
Code.query.delete()

# Add users

hashed = bcrypt.generate_password_hash("password")
password = hashed.decode("utf8")

jared = User(username="lorddreadman", email="jared_glenn@yahoo.com", first_name="Jared", last_name="Glenn", password=password)

db.session.add(jared)

db.session.commit()

# Add posts
response = Code(text="https://google.com", completed_code="/static/codes/response1.png", user_id=1)

db.session.add(response)

# Commit

db.session.commit()