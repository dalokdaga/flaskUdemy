from flask import Blueprint, render_template
from flask import request,flash,get_flashed_messages
from flask import abort, redirect, url_for
from my_app import db
from my_app.auth.model.user import User,UserForm

auth =  Blueprint('auth',__name__)

@auth.route('/register', methods=('GET', 'POST'))
def register():
   form = UserForm() 
   if form.validate_on_submit():  
      p = User(form.username.data,form.password.data)
      db.session.add(p)
      db.session.commit()    
      flash("Usuario creado con exito")      
      return redirect(url_for('auth.register'))

   if form.errors:
      flash(form.errors,"danger")     
   return render_template('auth/register.html',form = form)