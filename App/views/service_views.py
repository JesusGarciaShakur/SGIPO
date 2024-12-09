from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.service_forms import RegisterServiceForm, UpdateServiceForm, RegisterServiceRequestForm, UpdateServiceRequestForm
from models.services import Service, ServiceRequest
from models.clients import Client

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
        # Rango de paginación
        visible_pages = 5  # Número máximo de páginas visibles
        start_page = max(1, page - (visible_pages // 2))
        end_page = min(total_pages, start_page + visible_pages - 1)
        start_page = max(1, end_page - visible_pages + 1)  # Ajustar si estamos cerca del inicio
        
        return render_template('pages/service/service_list.html',
                            services=services,
                            page=page,
                            total_pages=total_pages,
                            start_page=start_page,
                            end_page=end_page)
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
            service.update()
            return redirect(url_for('service.service_list'))
        form.name_service.data = service.name_service
        form.description_service.data = service.description_service
        return render_template('pages/service/service_update.html', form=form, service=service)
    else:
        abort(403)

@service_views.route('/service/<int:id_service>/delete', methods=['POST'])
def service_delete(id_service):
    if session.get('user') and session.get('user')['type'] == 1:
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

#id_request, id_service, id_client, date_request, price_request
@service_views.route('/service_request_list')
def service_request_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            service_requests, total = ServiceRequest.search(search_query, page, per_page)
        else:
            service_requests, total = ServiceRequest.get_paginated_service_requests(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        # Rango de paginación
        visible_pages = 5  # Número máximo de páginas visibles
        start_page = max(1, page - (visible_pages // 2))
        end_page = min(total_pages, start_page + visible_pages - 1)
        start_page = max(1, end_page - visible_pages + 1)  # Ajustar si estamos cerca del inicio
        
        return render_template('pages/service/service_request_list.html',
                            service_requests=service_requests,
                            page=page, total_pages=total_pages,
                            start_page=start_page,
                            end_page=end_page)
    else:
        abort(403)
#id_request, id_service, id_client, date_request, price_request
@service_views.route('/service_request_register', methods=['GET', 'POST'])
def service_request_register():
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterServiceRequestForm()
        clients = Client.get_all()
        services = Service.get_all()
        form.id_service.choices = [(service.id_service, service.name_service) for service in services]
        form.id_client.choices = [(client.id_client, f"{client.name_client} {client.lastName_client}") for client in clients]
        if form.validate_on_submit():
            id_service = form.id_service.data
            id_client = form.id_client.data
            date_request = form.date_request.data
            price_request = form.price_request.data
            service_request = ServiceRequest(id_service=id_service, id_client=id_client, date_request=date_request, price_request=price_request)
            service_request.save()
            return redirect(url_for('service.service_request_list'))
        return render_template('pages/service/service_request_register.html', form=form, clients=clients, services=services)
    else:
        abort(403)
#id_request, id_service, id_client, date_request, price_request
@service_views.route('/service_request/<int:id_request>/edit', methods=['GET', 'POST'])
def service_request_update(id_request):
    if session.get('user') and session.get('user')['type'] == 1:
        form = UpdateServiceRequestForm()
        clients = Client.get_all()
        services = Service.get_all()
        form.id_service.choices = [(service.id_service, service.name_service) for service in services]
        form.id_client.choices = [(client.id_client, f"{client.name_client} {client.lastName_client}") for client in clients]
        service_request = ServiceRequest.get(id_request)
        if form.validate_on_submit():
            service_request.id_service = form.id_service.data
            service_request.id_client = form.id_client.data
            service_request.date_request = form.date_request.data
            service_request.price_request = form.price_request.data
            service_request.update()
            return redirect(url_for('service.service_request_list'))
        form.id_service.data = service_request.id_service
        form.id_client.data = service_request.id_client
        form.date_request.data = service_request.date_request
        form.price_request.data = service_request.price_request
        return render_template('pages/service/service_request_update.html', form=form, service_request=service_request, clients=clients, services=services)
    else:
        abort(403)

@service_views.route('/service_request/<int:id_request>/delete', methods=['POST'])
def service_request_delete(id_request):
    if session.get('user') and session.get('user')['type'] == 1:
        service_request = ServiceRequest.get(id_request)
        service_request.delete()
        return redirect(url_for('service.service_request_list'))
    
@service_views.route('/get_service_requests')
def get_service_requests():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    service_requests, total = ServiceRequest.get_paginated_services(page, per_page)

    service_requests_dict = [
        {
            'id_request': service_request.id_request,
            'id_service': service_request.id_service,
            'id_client': service_request.id_client,
            'date_request': service_request.date_request,
            'price_request': service_request.price_request,
        }
        for service_request in service_requests
    ]
    response = make_response(jsonify({'clients':service_requests_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response