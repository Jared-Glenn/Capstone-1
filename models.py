"""User and Feedback models detailed."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)
    
    
class User(db.Model):
    """User model."""
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20),
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(),
                      unique=True,
                      nullable=False)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    password = db.Column(db.String(),
                         nullable=False)
    
    codes = db.relationship("Code")
        
    def __repr__(self):
        return f"<User {self.id} {self.username} {self.first_name} {self.last_name} {self.codes} >"
 
 
class Code(db.Model):
    """Task model."""
    
    __tablename__ = "codes"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    text = db.Column(db.String(),
            nullable=False)
    completed_code = db.Column(db.String(),
                               nullable=False)
    size = db.Column(db.Integer,
                    nullable=True)
    logo_url = db.Column(db.String(),
                        nullable=True)
    gradient_type = db.Column(db.String(),
                              nullable=True)
    block_style = db.Column(db.Integer,
                            nullable=True)
    gradient = db.Column(db.Integer,
                        nullable=True)
    gradient_color_start = db.Column(db.String(10),
                                    nullable=True)
    gradient_color_end = db.Column(db.String(10),
                                    nullable=True)
    fg_color = db.Column(db.String(10),
                        nullable=True)
    bg_color = db.Column(db.String(10),
                        nullable=True)
    eye_style = db.Column(db.String(),
                            nullable=True)
    validate = db.Column(db.Integer,
                        nullable=True)
    logo_size = db.Column(db.Float,
                        nullable=True)
    
    user_id= db.Column(db.Integer,
                     db.ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)
    
    def __repr__(self):
        return f"<Task {self.id} {self.text} {self.completed_code} {self.user} >"
    