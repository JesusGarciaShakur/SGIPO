from flask import Blueprint, render_template, redirect

admin_views = Blueprint('admin', __name__)

@admin_views.route('/admin')
def admin():
    return render_template('pages/admin.html')

@admin_views.route('/admin_list')
def admin_list():
    return render_template('pages/listadmin.html')

@admin_views.route('/home')
def home():
    return render_template('pages/home.html')

@admin_views.route('/product')
def product():
    return render_template('pages/product.html')

@admin_views.route('/product_list')
def product_list():
    return render_template('pages/productlist.html')
