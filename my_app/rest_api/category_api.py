from flask.views import MethodView
from flask import request
from my_app import db
from my_app import app
import json
from my_app.product.model.category import Category
from my_app.rest_api.helper.request import  sendResJson


class CategoryApi(MethodView):
    def get(self, id=None):
        categories = Category.query.all()
        if id:
            category = Category.query.get(id)
            if not category:
                return sendResJson(None,"No existe categoria",403)
            res = categoryToJson(category)            
        else:                
            res = []
            for p in categories:
                res.append(categoryToJson(p))                                            
        return sendResJson(res,None,200)

    def post(self):
        if not request.form:
            return sendResJson(None,"sin parámetros",403)
        
        #validaciones nombre
        if not "name" in request.form:
            return sendResJson(None,"sin parámetros nombre",403)            
        if len(request.form['name']) < 3:
            return sendResJson(None,"Nombre no valido",403) 
        
        consulta =  Category.query.filter_by(name = request.form['name'] ).first()
        if consulta:
             return sendResJson(None,"El categoria ya existe",403)

        c = Category(request.form['name'])
        db.session.add(c)
        db.session.commit()
        return sendResJson(categoryToJson(c),None,200)

    def put(self,id):        
            
        if not request.form:
            return sendResJson(None,"sin parámetros",403)

        #validaciones nombre
        if not "name" in request.form:
            return sendResJson(None,"sin parámetros nombre",403)            
        if len(request.form['name']) < 3:
            return sendResJson(None,"Nombre no valido",403) 

        category = Category.query.get(id)
        if not category:
            return sendResJson(None,"El categoria no existe",403)                        

        category.name = request.form['name']
        db.session.add(category)
        db.session.commit()
        return sendResJson("categoria modificado",None,200)                               

    def delete(self,id):
        category = Category.query.get(id)
        if not category:
            return sendResJson(None,"El categoria no existe",403)                        
        else:
            try:
                db.session.delete(category)
                db.session.commit()                        
            except ValueError:
                return sendResJson(None,"No se puede eliminar",403)               
            return sendResJson("categoria eliminado",None,200)                               

def categoryToJson(category: Category):
    return {
        'id' : category.id,
        'name': category.name
    }

category_view = CategoryApi.as_view('category_view')
app.add_url_rule('/api/categories/',
view_func=category_view,
methods=['GET','POST'])
app.add_url_rule('/api/categories/<int:id>',
view_func=category_view,
methods=['GET','DELETE','POST','PUT'])
