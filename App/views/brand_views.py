from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.brand_forms import RegisterBrandForm, UpdateBrandForm
from models.brands import Brand, Supplier
from utils.file_handler import save_image

brand_views = Blueprint('brand', __name__)

@brand_views.route('/brand_list')
def brand_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            brands, total = Brand.search(search_query, page, per_page)
        else:
            brands, total = Brand.get_paginated_brands(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        return render_template('pages/brand/brand_list.html', brands=brands, page=page, total_pages=total_pages)
    else:
        abort(403)

@brand_views.route('/brand_register', methods=['GET', 'POST'])
def brand_register():
    #id_brand,name_brand ,description_brand ,id_supplier
    if session.get ('user') and session.get('user')['type'] == 1:
        form = RegisterBrandForm()
        suppliers = Supplier.get_all()
        form.id_supplier.choices = [(supplier.id_supplier, supplier.name_supplier) for supplier in suppliers]
        if form.validate_on_submit():
            name_brand = form.name_brand.data
            description_brand = form.description_brand.data
            id_supplier = form.id_supplier.data
            f = form.image_brand.data
            brand = Brand(name_brand=name_brand, description_brand=description_brand, id_supplier=id_supplier)
            if f:
                brand.image_brand = save_image(f, 'img/brands', brand.name_brand)
            brand.save()
            return redirect(url_for('brand.brand_list'))
        return render_template('pages/brand/brand_register.html', form=form)
    else:
        abort(403)

@brand_views.route('/brand/<int:id_brand>/edit', methods=['GET', 'POST'])
def brand_update(id_brand):
    if session.get('user') and session.get('user')['type'] == 1:
        form = UpdateBrandForm()
        suppliers = Supplier.get_all()
        form.id_supplier.choices = [(supplier.id_supplier, supplier.name_supplier) for supplier in suppliers]
        brand = Brand.get(id_brand)
        if form.validate_on_submit():
            brand.name_brand = form.name_brand.data
            brand.description_brand = form.description_brand.data
            brand.id_supplier = form.id_supplier.data
            f = form.image_brand.data
            if f:
                brand.image_brand = save_image(f, 'img/brands', brand.name_brand)
            else:
                brand.image_brand = brand.image_brand
            brand.update()
            return redirect(url_for('brand.brand_list'))
        form.name_brand.data = brand.name_brand
        form.description_brand.data = brand.description_brand
        form.id_supplier.data = brand.id_supplier
        return render_template('pages/brand/brand_update.html', form=form, brand=brand)
    else:
        abort(403)

@brand_views.route('/brand/<int:id_brand>/delete', methods=['POST'])
def brand_delete(id_brand):
    if session.get('user') and session.get('user')['type'] == 1:
        brand = Brand.get(id_brand)
        brand.delete()
        return redirect(url_for('brand.brand_list'))
    else:
        abort(403)

@brand_views.route('/get_brands')
def get_brands():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    brands, total = Brand.get_paginated_brands(page, per_page)

    brands_dict = [
        {
            'id_brand': brand.id_brand,
            'name_brand': brand.name_brand,
            'description_brand': brand.description_brand,
            'id_supplier': brand.id_supplier,
            'image_brand': brand.image_brand,
        }
        for brand in brands
    ]
    response = make_response(jsonify({'brands':brands_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response