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
    
    if "user_id" not in session:
        return redirect('/register')
    
    user_id = session["user_id"]
    
    return redirect(f'/users/{user_id}')
    

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



@app.route('/new-code/<user_id>', methods=["GET", "POST"])
async def new_code(user_id):
    """Route for creating a new code."""
    
    form = CodeForm()
    
    user = User.query.get_or_404(user_id)

    with open("static/codes/response1.png", 'rb') as f:
        print(f)
    
    if form.validate_on_submit():

        text = form.text.data
        form_dict = {'text': text, 'validate':0}
        
        if form.size.data:
            size = form.size.data
            form_dict["size"] = size
        else:
            size = None
            
        if form.logo_url.data:
            logo_url = form.logo_url.data
            form_dict["logo_url"] = logo_url
        else:
            logo_url = None
        
        if form.gradient_type.data:
            gradient_type = form.gradient_type.data
            form_dict["gradient_type"] = gradient_type
        else:
            gradient_type = None
        
        if form.block_style.data:
            block_style = form.block_style.data
            form_dict["block_style"] = block_style
        else:
            block_style = None
            
        if form.gradient.data:
            gradient = form.gradient.data
            form_dict["gradient"] = gradient
        else:
            gradient = None
            
        if form.gradient_color_start.data:
            gradient_color_start = form.gradient_color_start.data
            form_dict["gradient_color_start"] = gradient_color_start
        else:
            gradient_color_start = None
            
        if form.gradient_color_end.data:
            gradient_color_end = form.gradient_color_end.data
            form_dict["gradient_color_end"] = gradient_color_end
        else:
            gradient_color_end = None
            
        if form.fg_color.data:
            fg_color = form.fg_color.data
            form_dict["fg_color"] = fg_color
        else:
            fg_color = None
            
        if form.bg_color.data:
            bg_color = form.bg_color.data
            form_dict["bg_color"] = bg_color
        else:
            bg_color = None
            
        if form.eye_style.data:
            eye_style = form.eye_style.data
            form_dict["eye_style"] = eye_style
        else:
            eye_style = None
        
        if form.validate.data:
            validate = form.validate.data
            form_dict["validate"] = validate
        else:
            validate = None
            
        if form.logo_size.data:
            logo_size = form.logo_size.data
            form_dict["logo_size"] = logo_size
        else:
            logo_size = None
            
        print(form_dict)
        
        completed_code = await create_code(form_dict)
        print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{completed_code}!!!!!!!!!!!!!!!!!!!')
        
        new_code = Code(text=text,
                        completed_code=completed_code,
                        size=size,
                        logo_url=logo_url,
                        gradient_type=gradient_type,
                        block_style=block_style,
                        gradient=gradient,
                        gradient_color_start=gradient_color_start,
                        gradient_color_end=gradient_color_end,
                        fg_color=fg_color,
                        bg_color=bg_color,
                        eye_style=eye_style,
                        validate=validate,
                        logo_size=logo_size,
                        user_id=user_id)
        
        print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{new_code}!!!!!!!!!!!!!!!!!!!')
        
        db.session.add(new_code)
        db.session.commit()
        
        return redirect(f'/users/{user_id}')
        
    return render_template("new_code.html", form=form, user=user)



async def create_code(params):
    response = await asyncio.to_thread(requests.get,
                                       'https://qrcode-supercharged.p.rapidapi.com/',
                                       params=params,
                                       headers={
                                           'X-RapidAPI-Key': '39a572c804mshc607d739b32b3d7p1840eajsnb049ae15f5f7'
                                       })
    
    if response.ok:
        with open(f'static/codes/{response.headers["qrcode-file"]}', 'wb') as f:
            f.write(response.content)
        
        file_path = f'/static/codes/{response.headers["qrcode-file"]}'
        print(f'!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!{file_path}!!!!!!!!!!!!!!!!!!!')
        
        return file_path
    else:
        print(f'!!!RESPONSE HEADERS: {response.raise_for_status()}')
    


# @app.route('/test', methods=['GET'])
# async def index():
#     result = await hello()
#     return jsonify({"result": result})

# async def hello():
#     response = await asyncio.to_thread(requests.get, "https://pokeapi.co/api/v2/ability/1/")
#     return response.json()


@app.route('/logout')
def logout():
    """Logout route."""
    
    if "user_id" in session:
        session.pop("user_id")
    
    return redirect('/login')