from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('configuration.DevelopmentConfig')
db = SQLAlchemy(app)


from my_app.product.viewsProduct import product
from my_app.product.viewsCategory import category
from my_app.auth.views import auth
#importar vistas
app.register_blueprint(product)
app.register_blueprint(category)
app.register_blueprint(auth)
db.create_all()

@app.template_filter('mydouble')
def mydouble_filter(n:int):
    return n*2
#postgres
