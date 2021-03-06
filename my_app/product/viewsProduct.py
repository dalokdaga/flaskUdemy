from flask import Blueprint, render_template
from .model.products import PRODUCTS
from my_app.product.model.product import Product, ProductForm
from my_app.product.model.category import Category
from sqlalchemy.sql.expression import not_, or_
from my_app import db
from flask import request,flash,get_flashed_messages
from flask import abort, redirect, url_for
from flask_login import login_required
#from werkzeug import abort

product =  Blueprint('product',__name__)

@product.before_request
@login_required
def constructor():
   pass

@product.route('/')
@product.route('/home/<int:page>')
def index(page = 1):
   return render_template('product/index.html', products = Product.query.paginate(page,3))

@product.route('/product/<int:id>')
def show(id):      
   #product = Product.query.get_or_404(id)
   product = Product.query.get(id)
   if not product:
      return render_template('product/error.html')

   return render_template('product/show.html', product = product)

@product.route('/product-delete/<int:id>')
def delete(id):      
   product = Product.query.get_or_404(id)   
   db.session.delete(product)
   db.session.commit()   
   flash("Producto eliminado con exito")
   return redirect(url_for('product.index'))
   
#@product.route('/product/create')
#def create():
#   form = ProductForm()
#   #print(get_flashed_messages())
#   return render_template('product/create.html',form = form)

@product.route('/product/create', methods=('GET', 'POST'))
def create():
   #form = ProductForm(meta={'csrf':Flase})
   form = ProductForm()
   ##obtenemos todas las categorias para llenar el campo de selección
   categories = [ (c.id, c.name) for c in Category.query.all()]
   form.category_id.choices = categories
   ####
   if form.validate_on_submit():  
      p = Product(request.form['name'],request.form['price'],request.form['category_id'])
      db.session.add(p)
      db.session.commit()    
      flash("Producto creado con exito")      

   if form.errors:
      flash(form.errors,"danger")     
   return render_template('product/create.html',form = form)


#@product.route('/product/insert', methods =['POST'])
#def insert():
#   p = Product(request.form['name'],request.form['price'])
#   db.session.add(p)
#   db.session.commit()    
#   flash("Producto creado con exito")  
#   return redirect(url_for('product.create'))

@product.route('/test')
def test():      
   #p = Product.query.limit(2).all()
   #p = Product.query.limit(2).first() #primer registro
   #p = Product.query.order_by(Product.id.desc()).all() #primer registro
   #p = Product.query.get({"id":1}) # para busqueda llave primaria
   #p = Product.query.filter_by(name = "pistola").first() 
   #p = Product.query.filter(Product.id > 1).all()
   #p = Product.query.filter_by(name = "pistola", id = 2).first()
   #p = Product.query.filter(Product.name.like('p%')).all()
   #p = Product.query.filter(not_(Product.id > 1)).all()
   #p = Product.query.filter(or_(Product.id > 1, Product.name=="pistola")).all()
   #print(p)
   #crear
   #p = Product('P5',60.50)
   #db.session.add(p)
   #db.session.commit()
   #modificar
   #p = Product.query.filter_by(name = "pistola").first()
   #p.name = "UP1"
   #db.session.add(p)
   #db.session.commit()
   #borrar
   #p = Product.query.filter_by(name = "UP1").first()
   #db.session.delete(p)
   #db.session.commit()


   
   
   
   return "Flask"

@product.route('/filter/<int:id>')
def filter(id):
   product = PRODUCTS.get(id)
   return render_template('product/filter.html', product = product)
   

@product.app_template_filter('iva')
def iva_filter(product):
   if product["price"]:      
      return (product["price"] * .16) + product["price"]
   return "sin precio"   

@product.route('/product-edit/<int:id>')
def edit(id):
   product = Product.query.get_or_404(id)
   return render_template('product/edit.html',product = product)   

@product.route('/product-update/<int:id>', methods=['GET','POST'])
def update(id): 
   product = Product.query.get_or_404(id)  
   form = ProductForm()
   categories = [ (c.id, c.name) for c in Category.query.all()]   
   form.category_id.choices = categories      
   if request.method == 'GET':   
      form.name.data = product.name
      form.price.data = product.price
      form.category_id.data = product.category_id
   if form.validate_on_submit():    
      product.name = form.name.data
      product.price = form.price.data 
      product.category_id = form.category_id.data  
      db.session.add(product)
      db.session.commit()    
      flash("Producto actulizado con exito") 
      return redirect(url_for('product.update',id = product.id))
      if form.errors:
         flash(form.errors,"danger")         
      
   return render_template('product/update.html',product = product, form = form) 
