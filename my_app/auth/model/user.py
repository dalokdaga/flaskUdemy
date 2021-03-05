from sqlalchemy import Column, Integer, String
from my_app import db
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired, NumberRange, EqualTo
from my_app.product.model.product import Product

from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Enum
import enum

###esto es una prueba para el git
class RolUser(enum.Enum):
    regular = 1
    admin = 6

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(255))
    pwhash = db.Column(db.String(300))
    rol = db.Column(Enum(RolUser))

    def __init__(self, username, pwhash, rol = RolUser.regular):
        self.username = username        
        self.pwhash = generate_password_hash(pwhash)
        self.rol = rol    

    def __repr__(self):
        return '<Usuario %r>' % (self.username)
    
    def check_password(self,password):
        return check_password_hash(self.pwhash,password)        

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[InputRequired()])
    password = PasswordField('Repetir Password', validators=[InputRequired(),  EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password') 

class ChangePassword( FlaskForm):
    password = PasswordField('New Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')    