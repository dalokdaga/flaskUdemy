from flask import Blueprint, render_template
from flask import request,flash,get_flashed_messages
from flask import abort, redirect, url_for, session
from my_app import db
from my_app.auth.model.user import RegisterForm, LoginForm, User

auth =  Blueprint('auth',__name__)

@auth.route('/register', methods=('GET', 'POST'))
def register():
   
   ## validamos si esta logueado
   #if session.get('username'):
   if 'username' in session:
      print(session['username'])

   form = RegisterForm(meta={'csrf':False}) 
   if form.validate_on_submit():  
      c = User.query.filter_by(username = form.username.data).all()
      if c:
         flash("El usuario ya existe en el sistema","danger")               
      else:   
         p = User(form.username.data,form.password.data)
         db.session.add(p)
         db.session.commit()    
         flash("Usuario creado con exito")      
      return redirect(url_for('auth.register'))

   if form.errors:
      flash(form.errors,"danger")     
   return render_template('auth/register.html',form = form)

@auth.route('/login', methods=('GET', 'POST'))
def login():
   form = LoginForm(meta={'csrf':False}) 
   if form.validate_on_submit():  
      user = User.query.filter_by(username = form.username.data).first()
      if user and user.check_password(form.password.data):
         #registramos la sesion
         session['username'] = user.username
         session['id'] = user.id
         session['rol'] = user.rol.value
         flash("Bienvenido de nuevo " + user.username)      
         return redirect(url_for('product.index'))
      else:   
         flash("Usuario o contraseña incorrectos")      

   if form.errors:
      flash(form.errors,"danger")     
   return render_template('auth/login.html',form = form) 

@auth.route('/logout', methods=('GET', 'POST'))
def logout():
   session.pop('username', None)
   session.pop('id')
   session.pop('rol')
   return redirect(url_for('auth.login'))
