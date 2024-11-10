
from flask import Flask
#importar views
from views.admin_views import admin_views
app = Flask(__name__)
app.config['SECRET_KEY'] = 'My Secret Key'
#Registrar blueprints(views)
app.register_blueprint(admin_views)
if __name__ == '__main__':
    app.run(debug=True)
