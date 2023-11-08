from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField
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
    
    text = StringField("Code Text / Link",
                           validators=[InputRequired()])
    size = IntegerField("Size (Optional)",
                       validators=[Optional()])
    logo_size = FloatField("Size of Logo (Optional)",
                       validators=[Optional()])
    logo_url = StringField("URL for the Logo (Optional)",
                       validators=[Optional()])
    gradient_type = StringField("Gradient Type (Optional)",
                       validators=[Optional()])
    block_style = StringField("Block Style (Optional)",
                       validators=[Optional()])
    gradient = IntegerField("Gradient (Optional)",
                       validators=[Optional()])
    gradient_color_start = StringField("Starting Gradient Color Hex (Optional)",
                       validators=[Optional()])
    gradient_color_end = StringField("Ending Gradient Color Hex (Optional)",
                       validators=[Optional()])
    fg_color = StringField("Foreground Color Hex (Optional)",
                       validators=[Optional()])
    bg_color = StringField("Background Color Hex (Optional)",
                       validators=[Optional()])
    eye_style = StringField("Eye Style (Optional)",
                       validators=[Optional()])
    validate = IntegerField("Number of Validations (Optional)",
                       validators=[Optional()])
    
