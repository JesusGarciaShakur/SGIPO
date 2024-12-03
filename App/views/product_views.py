from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.product_forms import RegisterProductForm, UpdateProductForm
from models.products import Product, Brand

product_views = Blueprint('product', __name__)

@product_views.route('/product_list')
def product_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            products, total = Product.search(search_query, page, per_page)
        else:
            products, total = Product.get_paginated_products(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        return render_template('pages/product/product_list.html', products=products, page=page, total_pages=total_pages)
    else:
        abort(403)
    #id_product, name_product, description_product, id_brand, price_product, stock_product

@product_views.route('/product_register', methods=['GET', 'POST'])
def product_register():
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterProductForm()
        brands = Brand.get_all()
        form.id_brand.choices = [(brand.id_brand, brand.name_brand) for brand in brands]
        if form.validate_on_submit():
            name_product = form.name_product.data
            description_product = form.description_product.data
            id_brand = form.id_brand.data
            price_product = form.price_product.data
            stock_product = form.stock_product.data
            product = Product(name_product=name_product, description_product=description_product, id_brand=id_brand, price_product=price_product, stock_product=stock_product)
            product.save()
            return redirect(url_for('product.product_list'))
        return render_template('pages/product/product_register.html', form=form)
    else:
        abort(403)

@product_views.route('/product/<int:id_product>/update', methods=['GET', 'POST'])
def product_update(id_product):
    if session.get('user') and session.get('user')['type'] == 1:
        product = Product.get(id_product)
        form = UpdateProductForm()
        brands = Brand.get_all()
        form.id_brand.choices = [(brand.id_brand, brand.name_brand) for brand in brands]
        if form.validate_on_submit():
            product.name_product = form.name_product.data
            product.description_product = form.description_product.data
            product.id_brand = form.id_brand.data
            product.price_product = form.price_product.data
            product.stock_product = form.stock_product.data
            product.update()
            return redirect(url_for('product.product_list'))
        form.name_product.data = product.name_product
        form.description_product.data = product.description_product
        form.id_brand.data = product.id_brand
        form.price_product.data = product.price_product
        form.stock_product.data = product.stock_product
        return render_template('pages/product/product_update.html', form=form, product=product)
    else:
        abort(403)

@product_views.route('/product/<int:id_product>/delete', methods=['POST'])
def product_delete(id_product):
    if session.get('user') and session.get('user')['type'] == 1:
        product = Product.get(id_product)
        product.delete()
        return redirect(url_for('product.product_list'))
    else:
        abort(403)

@product_views.route('/get_products')
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    products, total = Product.get_paginated_products(page, per_page)

    products_dict = [
        {
            'id_product': product.id_product,
            'name_product': product.name_product,
            'description_product': product.description_product,
            'id_brand': product.id_brand,
            'price_product': product.price_product,
            'stock_product': product.stock_product,
        }
        for product in products
    ]
    response = make_response(jsonify({'products':products_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response