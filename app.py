"""Routes for each page."""

from flask import Flask, request, render_template, redirect, jsonify, session, flash
# from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
import requests
import asyncio
from models import db, connect_db, User, Code
from forms import RegisterForm, LoginForm, CodeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///qrcoder'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shhhh"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

bcrypt = Bcrypt()


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
        
        session["user_id"] = new_user.id
        
        return redirect(f'/users/{new_user.id}')
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
            
            session["user_id"] = user.id
            
            return redirect(f'/users/{user.id}')
        
        else:
            form.username.errors = ["Invalid username or password."]
            
    return render_template("login.html", form=form)




@app.route('/users/<user_id>')
def user(user_id):
    """User page."""

    
    if "user_id" not in session:
        flash("Please log in first!")
        
        return redirect('/login')
    
    if int(user_id) != session["user_id"]:
        
        print(f"page id: {user_id}")
        print(f"session id: {int(session['user_id'])}")
        
        flash("You can only access your own user page.")
        
        return redirect('/login')
    
    user = User.query.get_or_404(user_id)
    
    return render_template("user.html", user=user)



@app.route('/new-code/<user_id>')
def room(user_id):
    """Route for creating a new code."""
    
    form = CodeForm()
    
    if form.validate_on_submit():
        text = form.username.data
        completed_code = form.password.data
        
        user = User.query.get_or_404(user_id)
        
        if user and bcrypt.check_password_hash(user.password, password):
            
            session["user_id"] = user.id
            
            return redirect(f'/users/{user.id}')
        
        else:
            form.username.errors = ["Invalid username or password."]
            
    return render_template("new_code.html", form=form)


    # text = db.Column(db.String(),
    #         nullable=False)
    # completed_code = db.Column(db.String(),
    #                            nullable=False)
    # size = db.Column(db.Integer,
    #                 nullable=True)
    # logo_url = db.Column(db.String(),
    #                     nullable=True)
    # gradient_type = db.Column(db.String(),
    #                           nullable=True)
    # block_style = db.Column(db.Integer,
    #                         nullable=True)
    # gradient = db.Column(db.Integer,
    #                     nullable=True)
    # gradient_color_start = db.Column(db.String(10),
    #                                 nullable=True)
    # gradient_color_end = db.Column(db.String(10),
    #                                 nullable=True)
    # fg_color = db.Column(db.String(10),
    #                     nullable=True)
    # bg_color = db.Column(db.String(10),
    #                     nullable=True)
    # eye_style = db.Column(db.String(),
    #                         nullable=True)
    # validate = db.Column(db.Integer,
    #                     nullable=True)
    # logo_size = db.Column(db.Float,
    #                     nullable=True)
    
    # user_id= db.Column(db.Integer,
    #                  db.ForeignKey('users.id', ondelete='CASCADE'),
    #                  nullable=False)





@app.route('/test', methods=['GET'])
async def index():
    result = await hello()
    return jsonify({"result": result})

async def hello():
    response = await asyncio.to_thread(requests.get, "https://pokeapi.co/api/v2/ability/1/")
    return response.json()


@app.route('/logout')
def logout():
    """Logout route."""
    
    if "user_id" in session:
        session.pop("user_id")
    
    return redirect('/login')