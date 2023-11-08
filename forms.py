from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange, Length

class RegisterForm(FlaskForm):
    """Form for adding a new user."""
    
    username = StringField("Username",
                           validators=[Length(max=20, message="Username maximum length is 20 characters.")])
    password = PasswordField("Password")
    email = StringField("Email",
                        validators=[InputRequired(), Length(max=50, message="Email maximum length is 50 characters.")])
    first_name = StringField("First Name",
                             validators=[InputRequired(), Length(max=30, message="Name maximum length is 30 characters.")])
    last_name = StringField("Last Name",
                            validators=[InputRequired(), Length(max=30, message="Name maximum length is 30 characters.")])
    
    
class LoginForm(FlaskForm):
    """Form for logging in."""
    
    username = StringField("Username",
                           validators=[Length(max=20, message="Username maximum length is 20 characters.")])
    password = PasswordField("Password")
    

class CodeForm(FlaskForm):
    """Form for providing feedback from a specific user."""
    
    title = StringField("Title",
                           validators=[Length(max=100, message="Title maximum length is 100 characters.")])
    content = StringField("Feedback Content")
    


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