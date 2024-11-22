from flask import Flask
#importar views
from views.home_views import home_views
from views.admin_views import admin_views
from views.error_views import error_views
from views.client_views import client_views
app = Flask(__name__)
app.config['SECRET_KEY'] = 'My Secret Key'
#Registrar blueprints(views)
app.register_blueprint(home_views)
app.register_blueprint(admin_views)
app.register_blueprint(error_views)
app.register_blueprint(client_views)
if __name__ == '__main__':
    app.run(debug=True)
