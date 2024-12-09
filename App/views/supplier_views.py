from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.supplier_forms import RegisterSupplierForm, UpdateSupplierForm
from models.suppliers import Supplier

supplier_views = Blueprint('supplier', __name__)

@supplier_views.route('/supplier_list')
def supplier_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            suppliers, total = Supplier.search(search_query, page, per_page)
        else:
            suppliers, total = Supplier.get_paginated_suppliers(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        # Rango de paginación
        visible_pages = 5  # Número máximo de páginas visibles
        start_page = max(1, page - (visible_pages // 2))
        end_page = min(total_pages, start_page + visible_pages - 1)
        start_page = max(1, end_page - visible_pages + 1)  # Ajustar si estamos cerca del inicio
        
        return render_template('pages/supplier/supplier_list.html',
                            suppliers=suppliers,
                            page=page,
                            total_pages=total_pages,
                            start_page=start_page,
                            end_page=end_page)
    else:
        abort(403)

@supplier_views.route('/supplier_register', methods=['GET', 'POST'])
def supplier_register():
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterSupplierForm()
        if form.validate_on_submit():
            name_supplier = form.name_supplier.data
            direction_supplier = form.direction_supplier.data
            rfc_supplier = form.rfc_supplier.data
            contact_supplier = form.contact_supplier.data
            supplier = Supplier(name_supplier=name_supplier, direction_supplier=direction_supplier, rfc_supplier=rfc_supplier, contact_supplier=contact_supplier)
            supplier.save()
            return redirect(url_for('supplier.supplier_list'))
        return render_template('pages/supplier/supplier_register.html', form=form)
    else:
        abort(403)

@supplier_views.route('/supplier/<int:id_supplier>/update', methods=['GET', 'POST'])
def supplier_update(id_supplier):
    if session.get('user') and session.get('user')['type'] == 1:
        supplier = Supplier.get(id_supplier)
        form = UpdateSupplierForm()
        if form.validate_on_submit():
            supplier.name_supplier = form.name_supplier.data
            supplier.direction_supplier = form.direction_supplier.data
            supplier.rfc_supplier = form.rfc_supplier.data
            supplier.contact_supplier = form.contact_supplier.data
            supplier.update()
            return redirect(url_for('supplier.supplier_list'))
        form.name_supplier.data = supplier.name_supplier
        form.direction_supplier.data = supplier.direction_supplier
        form.rfc_supplier.data = supplier.rfc_supplier
        form.contact_supplier.data = supplier.contact_supplier
        return render_template('pages/supplier/supplier_update.html', form=form, supplier=supplier)
    else:
        abort(403)

@supplier_views.route('/supplier/<int:id_supplier>/delete', methods=['POST'])
def supplier_delete(id_supplier):
    if session.get('user') and session.get('user')['type'] == 1:
        supplier = Supplier.get(id_supplier)
        supplier.delete()
        return redirect(url_for('supplier.supplier_list'))
    else:
        abort(403)

@supplier_views.route('/get_suppliers')
def get_suppliers():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    suppliers, total = Supplier.get_paginated_suppliers(page, per_page)

    suppliers_dict = [
        {
            'id_supplier': supplier.id_supplier,
            'name_supplier': supplier.name_supplier,
            'direction_supplier': supplier.direction_supplier,
            'rfc_supplier': supplier.rfc_supplier,
            'contact_supplier': supplier.contact_supplier,
        }
        for supplier in suppliers
    ]
    response = make_response(jsonify({'suppliers':suppliers_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response