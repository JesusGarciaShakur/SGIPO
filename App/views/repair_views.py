from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.repair_forms import RegisterRepairForm
from models.repairs import Repair

repair_views = Blueprint('repair', __name__)

@repair_views.route('/repair_list')
def repair_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            repairs, total = Repair.search(search_query, page, per_page)
        else:
            repairs, total = Repair.get_paginated_repairs(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        # Rango de paginación
        visible_pages = 5  # Número máximo de páginas visibles
        start_page = max(1, page - (visible_pages // 2))
        end_page = min(total_pages, start_page + visible_pages - 1)
        start_page = max(1, end_page - visible_pages + 1)  # Ajustar si estamos cerca del inicio
        
        return render_template('pages/repair/repair_list.html',
                            repairs=repairs, page=page,
                            total_pages=total_pages,
                            start_page=start_page,
                            end_page=end_page)
    else:
        abort(403)
#id_repair, objectName_repair, quantity_repaired, cost_repair, date_repair
@repair_views.route('/repair_register', methods=['GET', 'POST'])
def repair_register():
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterRepairForm()
        if form.validate_on_submit():
            objectName_repair = form.objectName_repair.data
            quantity_repaired = form.quantity_repaired.data
            cost_repair = form.cost_repair.data
            date_repair = form.date_repair.data
            repair = Repair(objectName_repair=objectName_repair, quantity_repaired=quantity_repaired, cost_repair=cost_repair, date_repair=date_repair)
            repair.save()
            return redirect(url_for('repair.repair_list'))
        return render_template('pages/repair/repair_register.html', form=form)
    else:
        abort(403)

@repair_views.route('/get_repairs')
def get_repairs():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    repairs, total = Repair.get_paginated_repairs(page, per_page)

    repairs_dict = [
        {
            'id_repair': repair.id_repair,
            'objectName_repair': repair.objectName_repair,
            'quantity_repaired': repair.quantity_repaired,
            'cost_repair': repair.cost_repair,
            'date_repair': repair.date_repair,
        }
        for repair in repairs
    ]
    response = make_response(jsonify({'repairs':repairs_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response