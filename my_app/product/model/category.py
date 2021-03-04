from sqlalchemy import Column, Integer, String
from my_app import db
from decimal import Decimal
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, NumberRange
from my_app.product.model.product import Product
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(255))
    products = db.relationship('Product', backref='category', lazy= True)
    #products = db.relationship('Product', backref='category', lazy= 'select')
    #products = db.relationship('Product', backref='category', lazy= 'joined')
    #products = db.relationship('Product', backref='category', lazy= 'subquery')
    #products = db.relationship('Product', backref='category', lazy= 'dynamic')
    def __init__(self, name):
        self.name = name        

    def __repr__(self):
        return '<Category %r>' % (self.name)

class CategoryForm(FlaskForm):
    name = StringField('Nombre', validators=[InputRequired()])
    