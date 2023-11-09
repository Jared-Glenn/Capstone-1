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



@app.route('/new-code/<user_id>', methods=["GET", "POST"])
async def new_code(user_id):
    """Route for creating a new code."""
    
    form = CodeForm()
    
    user = User.query.get_or_404(user_id)

    with open("static/codes/response1.png", 'rb') as f:
        print(f)
    
    if form.validate_on_submit():

        text = form.text.data
        
        if form.size.data:
            size = form.size.data
        else:
            size = None
            
        if form.logo_url.data:
            logo_url = form.logo_url.data
        else:
            logo_url = None
        
        gradient_type = form.gradient_type.data
        block_style = form.block_style.data
        gradient = form.gradient.data
        gradient_color_start = form.gradient_color_start.data
        gradient_color_end = form.gradient_color_end.data
        fg_color = form.fg_color.data
        bg_color = form.bg_color.data
        eye_style = form.eye_style.data
        validate = form.validate.data
        logo_size = form.logo_size.data
        
        form_dict = {'size': size,
                    'logo_url': logo_url,
                    'gradient_type': gradient_type,
                    'block_style': block_style,
                    'gradient': gradient,
                    'gradient_color_start': gradient_color_start,
                    'gradient_color_end': gradient_color_end,
                    'fg_color': fg_color,
                    'bg_color': bg_color,
                    'eye_style': eye_style,
                    'validate': validate,
                    'logo_size': logo_size
                     }
        
        print(form_dict)
        
        # completed_code = await create_code(text,
        #                                    size=size,
        #                                    logo_url=logo_url,
        #                                    gradient_type=gradient_type,
        #                                    block_style=block_style,
        #                                    gradient=gradient,
        #                                    gradient_color_start=gradient_color_start,
        #                                    gradient_color_end=gradient_color_end,
        #                                    fg_color=fg_color,
        #                                    bg_color=bg_color,
        #                                    eye_style=eye_style,
        #                                    validate=validate,
        #                                    logo_size=logo_size)
        
        # new_code = Code(text=text,
        #                 completed_code=completed_code,
        #                 size=size,
        #                 logo_url=logo_url,
        #                 gradient_type=gradient_type,
        #                 block_style=block_style,
        #                 gradient=gradient,
        #                 gradient_color_start=gradient_color_start,
        #                 gradient_color_end=gradient_color_end,
        #                 fg_color=fg_color,
        #                 bg_color=bg_color,
        #                 eye_style=eye_style,
        #                 validate=validate,
        #                 logo_size=logo_size,
        #                 user_id=user_id)
        # db.session.add(new_code)
        # db.session.commit()
        
        return redirect(f'/users/{user_id}')
        
            
    return render_template("new_code.html", form=form, user=user)



async def create_code(text,
                      size = 400,
                      logo_url = 'https://cdn.auth0.com/blog/symfony-blog/logo.png',
                      gradient_type = 'diagonal',
                      block_style = 'square',
                      gradient = '1',
                      gradient_color_start = 'FF0000',
                      gradient_color_end = '00FF00',
                      fg_color = 'FF0000',
                      bg_color = 'FFFFFF',
                      eye_style = 'square',
                      validate = '1',
                      logo_size = '0.22'):
    
    print(f'text: {text}')
    print(f'size: {size}')
    print(f'logo_url: {logo_url}')
    print(f'fg_color: {fg_color}')
    print(f'bg_color: {bg_color}')
    print(f'eye_style: {eye_style}')
    print(f'validate: {validate}')
    # response = await asyncio.to_thread(requests.get,
    #                                    'https://qrcode-supercharged.p.rapidapi.com/',
    #                                    params={
    #                                        'text': text,
    #                                        'size': size,
    #                                        'logo_url': logo_url,
    #                                        'gradient_type': gradient_type,
    #                                        'block_style': block_style,
    #                                        'gradient': gradient,
    #                                        'gradient_color_start': gradient_color_start,
    #                                        'gradient_color_end': gradient_color_end,
    #                                        'fg_color': fg_color,
    #                                        'bg_color': bg_color,
    #                                        'eye_style': eye_style,
    #                                        'validate': validate,
    #                                        'logo_size': logo_size
    #                                    },
    #                                    headers={
    #                                        'X-RapidAPI-Key': '39a572c804mshc607d739b32b3d7p1840eajsnb049ae15f5f7'
    #                                    })
    
    # print(response.headers)

    # with open(f'static/codes/{response.headers["qrcode-file"]}', 'wb') as f:
    #     f.write(response.content)
        
    # return f'static/codes/{response.headers["qrcode-file"]}'
    return 1

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