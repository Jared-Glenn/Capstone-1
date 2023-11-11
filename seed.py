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
response2 = Code(text="www.springboard.com", completed_code="/static/codes/generated8376631.png", user_id=1)
response3 = Code(text="http://jaredglenn.herokuapp.com/", completed_code="/static/codes/generated6557772.png", user_id=1)
response4 = Code(text="https://www.aonprd.com/", completed_code="/static/codes/generated2621530.png", user_id=1)

db.session.add(response)
db.session.add(response2)
db.session.add(response3)
db.session.add(response4)

# Commit

db.session.commit()