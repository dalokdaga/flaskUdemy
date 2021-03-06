from flask import Blueprint, render_template
from my_app.product.model.category import Category,CategoryForm
from sqlalchemy.sql.expression import not_, or_
from my_app import db
from flask import request,flash,get_flashed_messages
from flask import abort, redirect, url_for
from flask_login import login_required
#from werkzeug import abort

category =  Blueprint('category',__name__)

@category.before_request
@login_required
def constructor():
   pass


@category.route('/category')
@category.route('/category/<int:page>')
def index(page = 1):
   return render_template('category/index.html', categories = Category.query.paginate(page,3))

@category.route('/category/<int:id>')
def show(id):      
   #categories = Category.query.get_or_404(id)
   categories = Category.query.get(id)
   if not categories:
      return render_template('category/error.html')

   return render_template('category/show.html', categories = categories)

@category.route('/category-delete/<int:id>')
def delete(id):      
   category = Category.query.get_or_404(id)   
   db.session.delete(category)
   db.session.commit()   
   flash("Categoria eliminado con exito")
   return redirect(url_for('category.index'))
   
#@categories.route('/categories/create')
#def create():
#   form = CategoryForm()
#   #print(get_flashed_messages())
#   return render_template('categories/create.html',form = form)

@category.route('/category/create', methods=('GET', 'POST'))
def create():
   #form = CategoryForm(meta={'csrf':Flase})
   form = CategoryForm()
   if form.validate_on_submit():  
      p = Category(request.form['name'])
      db.session.add(p)
      db.session.commit()    
      flash("Categoria creado con exito")      

   if form.errors:
      flash(form.errors,"danger")     
   return render_template('category/create.html',form = form)


#@categories.route('/categories/insert', methods =['POST'])
#def insert():
#   p = Category(request.form['name'],request.form['price'])
#   db.session.add(p)
#   db.session.commit()    
#   flash("Categoryo creado con exito")  
#   return redirect(url_for('categories.create'))
  

@category.route('/category-edit/<int:id>')
def edit(id):
   categories = Category.query.get_or_404(id)
   return render_template('categories/edit.html',categories = categories)   

@category.route('/category-update/<int:id>', methods=['GET','POST'])
def update(id): 
   category = Category.query.get_or_404(id)  
   form = CategoryForm()   
   if request.method == 'GET':   
      form.name.data = category.name

   if form.validate_on_submit():    
      category.name = form.name.data
      db.session.add(category)
      db.session.commit()    
      flash("Categoria actulizada con exito") 
      return redirect(url_for('category.update',id = category.id))
      if form.errors:
         flash(form.errors,"danger")         
      
   return render_template('category/update.html',category = category, form = form) 
