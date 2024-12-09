from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.sale_forms import RegisterSaleForm, UpdateSaleForm
from models.sales import Sale, Product, Client

sale_views = Blueprint('sale', __name__)

@sale_views.route('/sale_list')
def sale_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        
        if search_query:
            sales, total = Sale.search(search_query, page, per_page)
        else:
            sales, total = Sale.get_paginated_sales(page, per_page)
        
        total_pages = (total + per_page - 1) // per_page
        
        # Rango de paginación
        visible_pages = 5  # Número máximo de páginas visibles
        start_page = max(1, page - (visible_pages // 2))
        end_page = min(total_pages, start_page + visible_pages - 1)
        start_page = max(1, end_page - visible_pages + 1)  # Ajustar si estamos cerca del inicio
        
        return render_template(
            'pages/sale/sale_list.html',
            sales=sales,
            page=page,
            total_pages=total_pages,
            start_page=start_page,
            end_page=end_page
        )
    else:
        abort(403)
        
@sale_views.route('/sale_register', methods=['GET', 'POST'])
#id_sale,id_client,id_product,,quantity_sold,final_price,date_sold
def sale_register():
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterSaleForm()
        products = Product.get_all()
        form.id_product.choices = [(product.id_product, product.name_product) for product in products]
        clients = Client.get_all()
        form.id_client.choices = [(client.id_client, client.name_client) for client in clients]
        if form.validate_on_submit():
            id_client = form.id_client.data
            id_product = form.id_product.data
            quantity_sold = form.quantity_sold.data
            final_price = form.final_price.data
            date_sold = form.date_sold.data
            sale = Sale(id_client=id_client, id_product=id_product, quantity_sold=quantity_sold, final_price=final_price, date_sold=date_sold)
            sale.save()
            return redirect(url_for('sale.sale_list'))
        return render_template('pages/sale/sale_register.html', form=form)
    else:
        abort(403)

@sale_views.route('/sale/<int:id_sale>/update', methods=['GET', 'POST'])
def sale_update(id_sale):
    if session.get('user') and session.get('user')['type'] == 1:
        sale = Sale.get(id_sale)
        form = UpdateSaleForm(obj=sale)
        products = Product.get_all()
        form.id_product.choices = [(product.id_product, product.name_product) for product in products]
        clients = Client.get_all()
        form.id_client.choices = [(client.id_client, client.name_client) for client in clients]
        if form.validate_on_submit():
            sale.id_client = form.id_client.data
            sale.id_product = form.id_product.data
            sale.quantity_sold = form.quantity_sold.data
            sale.final_price = form.final_price.data
            sale.date_sold = form.date_sold.data
            sale.update()
            return redirect(url_for('sale.sale_list'))
        form.id_client.data = sale.id_client
        form.id_product.data = sale.id_product
        form.quantity_sold.data = sale.quantity_sold
        form.final_price.data = sale.final_price
        form.date_sold.data = sale.date_sold
        return render_template('pages/sale/sale_update.html', form=form, sale=sale)
    else:
        abort(403)

@sale_views.route('/sale/<int:id_sale>/delete', methods=['POST'])
def sale_delete(id_sale):
    if session.get('user') and session.get('user')['type'] == 1:
        sale = Sale.get(id_sale)
        sale.delete()
        return redirect(url_for('sale.sale_list'))
    else:
        abort(403)

@sale_views.route('/get_sales')
def get_sales():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    sales, total = Sale.get_paginated_sales(page, per_page)

    sales_dict = [
        {
            'id_sale': sale.id_sale,
            'id_client': sale.id_client,
            'id_product': sale.id_product,
            'quantity_sold': sale.quantity_sold,
            'final_price': sale.final_price,
            'date_sold': sale.date_sold
        }
        for sale in sales
    ]
    response = make_response(jsonify({'sales':sales_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response