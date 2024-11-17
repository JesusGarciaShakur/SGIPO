from flask import Blueprint, render_template, redirect, session, abort, url_for
from utils.file_handler import save_image
from forms.user_forms import RegisterUserForm
from models.users import User, Type

admin_views = Blueprint('admin', __name__)

@admin_views.route('/home')
def home():
    if session.get('user') and session.get('user')['type'] == 1:
        return render_template('pages/home.html')
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
            user.user_image = save_image(f, 'img/profiles', user.user_username)
        user.save()
        return redirect(url_for('admin.admin_list'))
    for field, errors in form.errors.items():
        for error in errors:
            print(f"Error en el campo '{field}': {error}")
    return render_template('pages/admin.html', form=form)

@admin_views.route('/admin_list')
def admin_list():
    return render_template('pages/listadmin.html')


@admin_views.route('/product')
def product():
    return render_template('pages/product.html')

@admin_views.route('/product_list')
def product_list():
    return render_template('pages/productlist.html')
