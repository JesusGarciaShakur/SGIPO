from flask import Flask
#importar views
from views.home_views import home_views
from views.admin_views import admin_views
from views.error_views import error_views
from views.client_views import client_views
from views.repair_views import repair_views
from views.service_views import service_views
from views.supplier_views import supplier_views
from views.brand_views import brand_views
from views.product_views import product_views
from views.purchase_views import purchase_views
from views.sale_views import sale_views
from views.return_views import return_views
app = Flask(__name__)
app.config['SECRET_KEY'] = 'My Secret Key'
#Registrar blueprints(views)
app.register_blueprint(home_views)
app.register_blueprint(admin_views)
app.register_blueprint(error_views)
app.register_blueprint(client_views)
app.register_blueprint(repair_views)
app.register_blueprint(service_views)
app.register_blueprint(supplier_views)
app.register_blueprint(brand_views)
app.register_blueprint(product_views)
app.register_blueprint(purchase_views)
app.register_blueprint(sale_views)
app.register_blueprint(return_views)
if __name__ == '__main__':
    app.run(debug=True)
