from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.purchase_forms import RegisterPurchaseForm, UpdatePurchaseForm
from models.purchases import Purchase, Product, Supplier

purchase_views = Blueprint('purchase', __name__)

@purchase_views.route('/purchase_list')
def purchase_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            purchases, total = Purchase.search(search_query, page, per_page)
        else:
            purchases, total = Purchase.get_paginated_purchases(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        # Rango de paginación
        visible_pages = 5  # Número máximo de páginas visibles
        start_page = max(1, page - (visible_pages // 2))
        end_page = min(total_pages, start_page + visible_pages - 1)
        start_page = max(1, end_page - visible_pages + 1)  # Ajustar si estamos cerca del inicio
        
        return render_template('pages/purchase/purchase_list.html',
                            purchases=purchases,
                            page=page,
                            total_pages=total_pages,
                            start_page=start_page,
                            end_page=end_page)
    else:
        abort(403)
    
@purchase_views.route('/purchase_register', methods=('GET', 'POST'))
def purchase_register():
    #id_purchase,id_supplier,id_product,,quantity_ordered,date_ordered
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterPurchaseForm()
        suppliers = Supplier.get_all()
        form.id_supplier.choices = [(supplier.id_supplier, supplier.name_supplier) for supplier in suppliers]
        products = Product.get_all()
        form.id_product.choices = [(product.id_product, product.name_product) for product in products]
        if form.validate_on_submit():
            id_supplier = form.id_supplier.data
            id_product = form.id_product.data
            quantity_ordered = form.quantity_ordered.data
            date_ordered = form.date_ordered.data
            purchase = Purchase(id_supplier=id_supplier, id_product=id_product, quantity_ordered=quantity_ordered, date_ordered=date_ordered)
            purchase.save()
            return redirect(url_for('purchase.purchase_list'))
        return render_template('pages/purchase/purchase_register.html', form=form)
    else:
        abort(403)

@purchase_views.route('/purchase/<int:id_purchase>/edit', methods=('GET', 'POST'))
def purchase_update(id_purchase):
    if session.get('user') and session.get('user')['type'] == 1:
        form = UpdatePurchaseForm()
        suppliers = Supplier.get_all()
        form.id_supplier.choices = [(supplier.id_supplier, supplier.name_supplier) for supplier in suppliers]
        products = Product.get_all()
        form.id_product.choices = [(product.id_product, product.name_product) for product in products]
        purchase = Purchase.get(id_purchase)
        if form.validate_on_submit():
            purchase.id_supplier = form.id_supplier.data
            purchase.id_product = form.id_product.data
            purchase.quantity_ordered = form.quantity_ordered.data
            purchase.date_ordered = form.date_ordered.data
            purchase.update()
            return redirect(url_for('purchase.purchase_list'))
        form.id_supplier.data = purchase.id_supplier
        form.id_product.data = purchase.id_product
        form.quantity_ordered.data = purchase.quantity_ordered
        form.date_ordered.data = purchase.date_ordered
        return render_template('pages/purchase/purchase_update.html', form=form, purchase=purchase)
    else:
        abort(403)

@purchase_views.route('/purchase/<int:id_purchase>/delete', methods=['POST'])
def purchase_delete(id_purchase):
    if session.get('user') and session.get('user')['type'] == 1:
        purchase = Purchase.get(id_purchase)
        purchase.delete()
        return redirect(url_for('purchase.purchase_list'))
    else:
        abort(403)

@purchase_views.route('/get_purchases')
def get_purchases():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    purchases, total = Purchase.get_paginated_purchases(page, per_page)

    purchases_dict = [
        {
            'id_purchase': purchase.id_purchase,
            'id_supplier': purchase.id_supplier,
            'id_product': purchase.id_product,
            'quantity_ordered': purchase.quantity_ordered,
            'date_ordered': purchase.date_ordered,
        }
        for purchase in purchases
    ]
    response = make_response(jsonify({'purchases':purchases_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response