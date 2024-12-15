# Importaciones
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from models.users import User
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField

#Clase para registro
class RegisterUserForm(FlaskForm):
    id_rol = SelectField('Tipo de Usuario', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un tipo de Usuario")])
    userName_user = StringField('Nombre(s)', validators = [DataRequired(), Length(min=4, max=25, message="El nombre de usuario ya esta en uso")])#
    name_user = StringField('Nombre de Usuario', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])#
    lastName_user = StringField('Apellido(s)', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])#
    password_user = PasswordField('Contraseña', validators = [DataRequired(message="Campo requerido"), Length(min=8)])#
    password_user_confirm = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password_user', message="Las contraseñas deben coincidir")])#
    numberPhone_user = StringField('Teléfono', validators = [DataRequired(), Length(min=10, max=10, message="Ingrese 10 caracteres (solo números)")])
    image_user = FileField('Imagen de Usuario', validators=[ FileAllowed(['png', 'jpg', 'jpeg'], 'Solo imágenes con extension png, jpg, jpeg!')])
    submit = SubmitField('Registrarse')
    
    #Validar username único
    def validate_userName_user(self, field):
        # Verifica si el nombre de usuario ha cambiado y si el nuevo nombre ya existe
        if field.data != self.userName_user:  # Compara si el nuevo username es diferente al actual
            if User.check_username(field.data):
                raise ValidationError('El username ya esta en uso')
        
#Clase para login
class LoginForms(FlaskForm):
    userName_user = StringField('Nombre de Usuario', validators=[DataRequired(message="Campo requerido")])
    password_user = PasswordField('Contraseña', validators=[DataRequired(message="Campo requerido")])
    submit = SubmitField('Ingresar')

#Clase para actualizar perfil
class UpdateUserForm(FlaskForm):
    id_rol = SelectField('Tipo de Usuario', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un tipo de Usuario")])
    name_user = StringField('Nombre de Usuario', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])
    lastName_user = StringField('Apellido(s)', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])
    numberPhone_user = StringField('Teléfono', validators = [DataRequired(), Length(min=10, max=10, message="Ingrese 10 caracteres (solo números)")])
    image_user = FileField('Imagen de Usuario', validators=[ FileAllowed(['png', 'jpg', 'jpeg'], 'Solo imágenes con extension png, jpg, jpeg!')])
    submit = SubmitField('Actualizar')


class UpdateUserInfo(FlaskForm):
    password_user = PasswordField('Contraseña', validators = [DataRequired(message="Campo requerido"), Length(min=8)])#
    password_user_confirm = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password_user', message="Las contraseñas deben coincidir")])#
    userName_user = StringField('Nombre de usuario', validators = [DataRequired(), Length(min=4, max=25)])
    submit = SubmitField('Actualizar información')