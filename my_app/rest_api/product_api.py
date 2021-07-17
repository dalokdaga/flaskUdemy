from flask.views import MethodView
from flask import request
from my_app.product.model.product import Product
from my_app import db
from my_app import app
import json
from my_app.product.model.category import Category
from my_app.rest_api.helper.request import  sendResJson


class ProductApi(MethodView):
    def get(self, id=None):
        products = Product.query.all()
        if id:
            product = Product.query.get(id)
            if not product:
                return sendResJson(None,"No existe producto",403)
            res = productToJson(product)

        else:                
            res = []
            for p in products:
                res.append(productToJson(p))

        return sendResJson(res,None,200)

    def post(self):
        if not request.form:
            return sendResJson(None,"sin parametros",403)
        
        #validaciones nombre
        if not "name" in request.form:
            return sendResJson(None,"sin parametros nombre",403)            
        if len(request.form['name']) < 3:
            return sendResJson(None,"Nombre no valido",403) 
        #validaciones precio
        if not "price" in request.form:
            return sendResJson(None,"sin parametros precio",403)                    
        try:
           float(request.form['price'])
        except ValueError:
            return sendResJson(None,"precio no valido",403)
             
        #validaciones categoria
        if not "category_id" in request.form:
            return sendResJson(None,"sin parámetros categoría",403)     
        
        category = Category.query.get(request.form['category_id'])
        if not category:
            return sendResJson(None,"categoria no existe",403)

        consultaProducto =  Product.query.filter_by(name = request.form['name'] ).first()
        if consultaProducto:
             return sendResJson(None,"El producto ya existe",403)

        p = Product(request.form['name'],request.form['price'],request.form['category_id'])
        db.session.add(p)
        db.session.commit()
        return sendResJson(productToJson(p),None,200)

    def put(self,id):        
            
        if not request.form:
            return sendResJson(None,"sin parámetros",403)

        #validaciones nombre
        if not "name" in request.form:
            return sendResJson(None,"sin parámetros nombre",403)            
        if len(request.form['name']) < 3:
            return sendResJson(None,"Nombre no valido",403) 
        #validaciones precio
        if not "price" in request.form:
            return sendResJson(None,"sin parametros precio",403)                    
        try:
           float(request.form['price'])
        except ValueError:
            return sendResJson(None,"precio no valido",403)
             
        #validaciones categoria
        if not "category_id" in request.form:
            return sendResJson(None,"sin parámetros categoría",403)     
        
        category = Category.query.get(request.form['category_id'])
        if not category:
            return sendResJson(None,"categoria no existe",403)

        product = Product.query.get(id)
        if not product:
            return sendResJson(None,"El producto no existe",403)                        

        product.name = request.form['name']
        product.price = request.form['price']
        product.category_id = request.form['category_id']
        db.session.add(product)
        db.session.commit()
        return sendResJson("Producto modificado",None,200)                               

    def delete(self,id):
        product = Product.query.get(id)
        if not product:
            return sendResJson(None,"El producto no existe",403)                        
        else:   
            db.session.delete(product)
            db.session.commit()            
            return sendResJson("Producto eliminado",None,200)                               

def productToJson(product: Product):
    return {
        'id' : product.id,
        'name': product.name,
        'id_category': product.category_id,
        'category': product.category.name
    }

product_view = ProductApi.as_view('product_view')
app.add_url_rule('/api/products/',
view_func=product_view,
methods=['GET','POST'])
app.add_url_rule('/api/products/<int:id>',
view_func=product_view,
methods=['GET','DELETE','POST','PUT'])
