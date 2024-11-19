from flask import Blueprint, jsonify, make_response, render_template, redirect, request, session, abort, url_for
from utils.file_handler import save_image
from forms.user_forms import RegisterUserForm, UpdateUserForm
from models.users import User, Type, count_users

admin_views = Blueprint('admin', __name__)

@admin_views.route('/home')
def home():
    if session.get('user') and session.get('user')['type'] == 1:
        total_users = count_users()
        return render_template('pages/home.html', total_users=total_users)
    else:
        abort(403)

@admin_views.route('/admin', methods=('GET', 'POST'))
def admin_register():
    #id_user, userName_user, password_user, id_rol, name_user, lastName_user, numberPhone_user, image_user
    form = RegisterUserForm()
    types = Type.get_all()
    form.id_rol.choices = [(type.id_rol, type.name_rol) for type in types]
    if form.validate_on_submit():
        userName_user = form.userName_user.data
        password_user = form.password_user.data
        id_rol = form.id_rol.data
        name_user = form.name_user.data
        lastName_user = form.lastName_user.data
        numberPhone_user = form.numberPhone_user.data
        f = form.image_user.data
        user = User(userName_user=userName_user, password_user=password_user, id_rol=id_rol, name_user=name_user, lastName_user=lastName_user, numberPhone_user=numberPhone_user)
        if f:
            user.image_user = save_image(f, 'img/profiles', user.userName_user)
        user.save()
        return redirect(url_for('admin.admin_list'))
    for field, errors in form.errors.items():
        for error in errors:
            print(f"Error en el campo '{field}': {error}")
    return render_template('pages/admin.html', form=form)

@admin_views.route('/admin_list')
def admin_list():
    if session.get('user') and session.get('user')['type'] == 1:
        page = int(request.args.get('page', 1))
        per_page = 10
        search_query = request.args.get('search', '')
        if search_query:
            users, total = User.search(search_query, page, per_page)
        else:
            users, total = User.get_paginated_users(page, per_page)
        total_pages = (total + per_page - 1) // per_page
        return render_template('pages/listadmin.html', users=users, page=page, total_pages=total_pages)
    else:
        abort(403)

@admin_views.route('/get_users')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    users, total = User.get_paginated_users(page, per_page)

    users_dict = [
        {
            'id_rol': user.id_rol,
            'userName_user': user.userName_user,
            'name_user': user.name_user,
            'lastName_user': user.lastName_user,
            'numberPhone_user': user.numberPhone_user,
            'image_user': user.image_user,
        }
        for user in users
    ]

    response = make_response(jsonify({'users':users_dict, 'total': total, 'page': page, 'per_page': per_page}))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@admin_views.route('/admin/users/<int:id_user>/edit', methods=['GET', 'POST'])
def admin_update_users(id_user):
    if session.get('user') and session.get('user')['type'] == 1:
        form = UpdateUserForm()
        types = Type.get_all()
        form.id_rol.choices = [(type.id_rol, type.name_rol) for type in types]
        user = User.get(id_user)
        if form.validate_on_submit():
            user.id_rol = form.id_rol.data
            user.userName_user = form.userName_user.data
            user.name_user = form.name_user.data
            user.lastName_user = form.lastName_user.data
            user.password_user = form.password_user.data
            user.numberPhone_user = form.numberPhone_user.data
            f = form.image_user.data
            if f:
                user.image_user = save_image(f, 'img/profiles', user.userName_user)
            else:
                user.image_user = user.image_user  # Mantener valor existente si no hay imagen nueva
            user.update()
            return redirect(url_for('admin.admin_list'))
        
        form.id_rol.data = user.id_rol
        form.userName_user.data = user.userName_user
        form.name_user.data = user.name_user
        form.lastName_user.data = user.lastName_user
        form.password_user.data = user.password_user
        form.numberPhone_user.data = user.numberPhone_user
        return render_template('pages/admin_update.html', form=form, user=user)
    else:
        abort(403)

@admin_views.route('/admin/users/<int:id_user>/delete', methods=['POST'])
def admin_delete_users(id_user):
    if session.get('user') and session.get('user')['type'] == 1:
        user = User.get(id_user)
        user.delete()
        return redirect(url_for('admin.admin_list'))
    else:
        abort(403)

@admin_views.route('/product')
def product():
    return render_template('pages/product.html')

@admin_views.route('/product_list')
def product_list():
    return render_template('pages/productlist.html')
