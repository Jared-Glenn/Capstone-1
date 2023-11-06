"""Routes for each page."""

from flask import Flask, request, render_template, redirect, jsonify, session, flash
# from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Code
from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///qrcoder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

# connect_db(app)
# app.app_context().push()
# db.create_all()

# bcrypt = Bcrypt()


# Main page

@app.route('/')
def home():
    """User homepage. Redirects to Register."""
    
    return redirect('/register')


# Registration page

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register a new user."""
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        hashed = bcrypt.generate_password_hash(form.password.data)
        password = hashed.decode("utf8")
        
        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        
        session["username"] = new_user.username
        
        return redirect(f'/users/{new_user.username}')
    else:
        return render_template("register.html", form=form)

# Login page

@app.route('/login', methods=["GET", "POST"])
def login():
    """Login to site."""
    
    form =LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            
            session["username"] = user.username
            
            return redirect(f'/users/{username}')
        
        else:
            form.username.errors = ["Invalid username or password."]
            
    return render_template("login.html", form=form)




@app.route('/')
def desk():
    """Register page."""
    
    user = User.query.get_or_404(1)
    
    rooms = []
    for room in user.rooms:
        rooms.append(room.name)
    events = (Event
              .query
              .filter(Event.room.in_(rooms))
              .order_by(Event.datetime.desc())
              .limit(100)
              .all())
    
    return render_template("desk.html", user=user, events=events)


@app.route('/floorplan')
def floorplan():
    """User floorplan."""
    
    user = User.query.get_or_404(1)
    
    return render_template("floorplan.html", user=user)


@app.route('/roomz/<room_id>')
def room(room_id):
    """Room."""
    
    user = User.query.get_or_404(1)
    room = Room.query.get_or_404(room_id)
    
    # Get all teammates.
    teammate_list = (User_Room
                 .query
                 .filter(User_Room.room_id == room_id)
                 .limit(10)
                 .all())
    
    teammate_ids = []
    for teammate in teammate_list:
        teammate_ids.append(teammate.user_id)
    
    teammates = (User
                .query
                .filter(User.id.in_(teammate_ids))
                .all())
    
    events = Event.query.filter(Event.room==room.name)
    
    return render_template("room.html", user=user, room=room, teammates=teammates, events=events)
