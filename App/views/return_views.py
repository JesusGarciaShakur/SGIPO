from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.return_forms import RegisterReturnForm, UpdateReturnForm
from models.returns import Sale, Return

return_views = Blueprint('return', __name__)

@return_views.route('/return_list')
def return_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            returns, total = Return.search(search_query, page, per_page)
        else:
            returns, total = Return.get_paginated_returns(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        visible_pages = 5  # Número máximo de páginas visibles
        start_page = max(1, page - (visible_pages // 2))
        end_page = min(total_pages, start_page + visible_pages - 1)
        start_page = max(1, end_page - visible_pages + 1)  # Ajustar si estamos cerca del inicio
        
        return render_template('pages/return/return_list.html',
                            returns=returns,
                            page=page,
                            total_pages=total_pages,
                            start_page=start_page,
                            end_page=end_page)
    else:
        abort(403)

@return_views.route('/return_register', methods=['GET', 'POST'])
def return_register():
    #id_return,id_sale,reason,date_return
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterReturnForm()
        sales = Sale.get_all()
        form.id_sale.choices = [(sale.id_sale, sale.id_sale) for sale in sales]
        if form.validate_on_submit():
            id_sale = form.id_sale.data
            reason = form.reason.data
            date_return = form.date_return.data
            return_ = Return(id_sale=id_sale, reason=reason, date_return=date_return)
            return_.save()
            return redirect(url_for('return.return_list'))
        return render_template('pages/return/return_register.html', form=form)
    else:
        abort(403)

@return_views.route('/return/<int:id_return>/update', methods=['GET', 'POST'])
def return_update(id_return):
    if session.get('user') and session.get('user')['type'] == 1:
        return_ = Return.get(id_return)
        form = UpdateReturnForm()
        sales = Sale.get_all()
        form.id_sale.choices = [(sale.id_sale, sale.id_sale) for sale in sales]
        if form.validate_on_submit():
            return_.id_sale = form.id_sale.data
            return_.reason = form.reason.data
            return_.date_return = form.date_return.data
            return_.update()
            return redirect(url_for('return.return_list'))
        form.id_sale.data = return_.id_sale
        form.reason.data = return_.reason
        form.date_return.data = return_.date_return
        return render_template('pages/return/return_update.html', form=form, return_=return_)
    else:
        abort(403)

@return_views.route('/return/<int:id_return>/delete', methods=['POST'])
def return_delete(id_return):
    if session.get('user') and session.get('user')['type'] == 1:
        return_ = Return.get(id_return)
        return_.delete()
        return redirect(url_for('return.return_list'))
    else:
        abort(403)

@return_views.route('/get_returns')
def get_returns():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    returns, total = Return.get_paginated_returns(page, per_page)

    returns_dict = [
        {
            'id_return': return_.id_return,
            'id_sale': return_.id_sale,
            'reason': return_.reason,
            'date_return': return_.date_return,
        }
        for return_ in returns
    ]
    response = make_response(jsonify({'returns':returns_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response