from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from forms.client_forms import RegisterClientForm, UpdateClientForm
from models.clients import Client, Disease

client_views = Blueprint('client', __name__)

@client_views.route('/client_list')
def client_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            clients, total = Client.search(search_query, page, per_page)
        else:
            clients, total = Client.get_paginated_clients(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        # Rango de paginación
        visible_pages = 5  # Número máximo de páginas visibles
        start_page = max(1, page - (visible_pages // 2))
        end_page = min(total_pages, start_page + visible_pages - 1)
        start_page = max(1, end_page - visible_pages + 1)  # Ajustar si estamos cerca del inicio
        return render_template('pages/client/client_list.html',
                            clients=clients,
                            page=page,
                            total_pages=total_pages,
                            start_page=start_page,
                            end_page=end_page)
    else:
        abort(403)

@client_views.route('/client_register', methods=('GET', 'POST'))
def client_register():
    # id_client, name_client, lastName_client, age_client, numberPhone_client, email_client, direction_client, id_disease
    if session.get('user') and session.get('user')['type'] == 1:
        form = RegisterClientForm()
        diseases = Disease.get_all()
        form.id_disease.choices = [(disease.id_disease, disease.name_disease) for disease in diseases]
        if form.validate_on_submit():
            name_client = form.name_client.data
            lastName_client = form.lastName_client.data
            age_client = form.age_client.data
            numberPhone_client = form.numberPhone_client.data
            email_client = form.email_client.data
            direction_client = form.direction_client.data
            id_disease = form.id_disease.data    
            client = Client(name_client=name_client, lastName_client=lastName_client, age_client=age_client, numberPhone_client=numberPhone_client, email_client=email_client, direction_client=direction_client, id_disease=id_disease)
            client.save()
            return redirect(url_for('client.client_list'))
        return render_template('pages/client/client_register.html', form=form)
    else:
        abort(403)

@client_views.route('/client/<int:id_client>/edit', methods=('GET', 'POST'))
def client_update(id_client):
    if session.get('user') and session.get('user')['type'] == 1:
        form = UpdateClientForm()
        diseases = Disease.get_all()
        form.id_disease.choices = [(disease.id_disease, disease.name_disease) for disease in diseases]
        client = Client.get(id_client)
        if form.validate_on_submit():
            client.name_client = form.name_client.data
            client.lastName_client = form.lastName_client.data
            client.age_client = form.age_client.data
            client.numberPhone_client = form.numberPhone_client.data
            client.email_client = form.email_client.data
            client.direction_client = form.direction_client.data
            client.id_disease = form.id_disease.data
            client.update()
            return redirect(url_for('client.client_list'))
        form.name_client.data = client.name_client
        form.lastName_client.data = client.lastName_client
        form.age_client.data = client.age_client
        form.numberPhone_client.data = client.numberPhone_client
        form.email_client.data = client.email_client
        form.direction_client.data = client.direction_client
        form.id_disease.data = client.id_disease
        return render_template('pages/client/client_update.html', form=form, client=client)
    else:
        abort(403)

@client_views.route('/client/<int:id_client>/delete', methods=['POST'])
def client_delete(id_client):
    if session.get('user') and session.get('user')['type'] == 1:
        client = Client.get(id_client)
        client.delete()
        return redirect(url_for('client.client_list'))
    else:
        abort(403)

@client_views.route('/get_clients')
def get_clients():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    clients, total = Client.get_paginated_users(page, per_page)

    clients_dict = [
        {
            'id_client': client.id_client,
            'name_client': client.name_client,
            'lastName_client': client.lastName_client,
            'age_client': client.age_client,
            'numberPhone_client': client.numberPhone_client,
            'email_client': client.email_client,
            'direction_client': client.direction_client,
            'id_disease': client.id_disease,
        }
        for client in clients
    ]

    response = make_response(jsonify({'clients':clients_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response