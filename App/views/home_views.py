from flask import Blueprint, render_template, redirect, url_for, flash, session
from models.users import User
from forms.user_forms import LoginForms

home_views = Blueprint('home', __name__)

@home_views.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForms()
    if form.validate_on_submit():
        userName_user = form.userName_user.data
        password_user = form.password_user.data
        user = User.get_by_password(userName_user, password_user)
        if not user:
            flash('Verifica tus Datos')
        else:
            #id_user, userName_user, password_user, id_rol, name_user, lastName_user, numberPhone_user, image_user
            session['user'] = {
                'id_user': user.id_user,
                'userName_user': user.userName_user,
                'type': user.id_rol,
                'name_user': user.name_user,
                'lastName_user': user.lastName_user,
                'numberPhone_user': user.numberPhone_user,
                'image_user': user.image_user
            }
            if user.id_rol == 1:
                return redirect(url_for('admin.home'))
            else:
                flash('Nombre de usuario o contraseña incorrectos', 'error')
    else:
        flash('Verifica tus Datos')
    return render_template('pages/home/login.html', form=form)

@home_views.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()  # Elimina todos los datos de la sesión
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('home.login'))  # Redirige al formulario de inicio de sesión