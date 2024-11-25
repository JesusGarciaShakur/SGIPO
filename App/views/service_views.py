from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.service_forms import RegisterServiceForm,  UpdateServiceForm
from models.services import Service

service_views = Blueprint('service', __name__)
#id_service, name_service, description_service
@service_views.route('/service_list')
def service_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            services, total = Service.search(search_query, page, per_page)
        else:
            services, total = Service.get_paginated_services(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        return render_template('pages/service/service_list.html', services=services, page=page, total_pages=total_pages)
    else:
        abort(403)

@service_views.route('/service_register', methods=['GET', 'POST'])
def service_register():
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterServiceForm()
        if form.validate_on_submit():
            name_service = form.name_service.data
            description_service = form.description_service.data
            service = Service(name_service=name_service, description_service=description_service)
            service.save()
            return redirect(url_for('service.service_list'))
        return render_template('pages/service/service_register.html', form=form)
    else:
        abort(403)

@service_views.route('/service/<int:id_service>/edit', methods=['GET', 'POST'])
def service_update(id_service):
    if session.get('user') and session.get('user')['type'] == 1:
        service = Service.get(id_service)
        form = UpdateServiceForm(obj=service)
        if form.validate_on_submit():
            service.name_service = form.name_service.data
            service.description_service = form.description_service.data
            service.save()
            return redirect(url_for('service.service_list'))
        form.name_service.data = service.name_service
        form.description_service.data = service.description_service
        return render_template('pages/service/service_update.html', form=form, service=service)
    else:
        abort(403)

@service_views.route('/service/<int:id_service>/delete', methods=['POST'])
def service_delete(id_service):
    if session('user') and session.get('user')['type'] == 1:
        service = Service.get(id_service)
        service.delete()
        return redirect(url_for('service.service_list'))
    else:
        abort(403)

@service_views.route('/get_services')
def get_services():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    services, total = Service.get_paginated_services(page, per_page)

    services_dict = [
        {
            'id_service': service.id_service,
            'name_service': service.name_service,
            'description_service': service.description_service,
        }
        for service in services
    ]
    response = make_response(jsonify({'clients':services_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response