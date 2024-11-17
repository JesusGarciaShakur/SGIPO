# Importaciones
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField,ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from models.users import User
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField

#Clase para registro
class RegisterUserForm(FlaskForm):
    #id_user, userName_user, password_user, id_rol, name_user, lastName_user, numberPhone_user, image_user
    id_rol = SelectField('Tipo de Usuario', coerce=int, choices=[])
    userName_user = StringField('Nombre(s)', validators = [DataRequired(), Length(min=4, max=25)])#
    name_user = StringField('Nombre de Usuario', validators = [DataRequired(), Length(min=4, max=25)])#
    lastName_user = StringField('Apellido(s)', validators = [DataRequired(), Length(min=4, max=25)])#
    password_user = PasswordField('Contraseña', validators = [DataRequired(), Length(min=8)])#
    password_user_confirm = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password_user')])#
    numberPhone_user = StringField('Teléfono', validators = [DataRequired(), Length(min=10, max=10)])
    image_user = FileField('Imagen de Usuario', validators=[ FileAllowed(['png', 'jpg'], 'Solo imágenes con extension png, jpg!')])
    submit = SubmitField('Registrarse')
        

    #Validar username único
    def validate_userName_user(self, field):
        if User.check_username(field.data):
            raise ValidationError('El username ya esta en uso')
        
#Clase para login
class LoginForms(FlaskForm):
    userName_user = StringField('Nombre de Usuario', validators=[DataRequired()])
    password_user = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

#Clase para actualizar perfil
class UpdateUserForm(FlaskForm):
    id_rol = SelectField('Tipo de Usuario', coerce=int, validators=[DataRequired()], choices=[])
    userName_user = StringField('Nombre(s)', validators = [DataRequired(), Length(min=4, max=25)])
    name_user = StringField('Nombre de Usuario', validators = [DataRequired(), Length(min=4, max=25)])
    lastName_user = StringField('Apellido(s)', validators = [DataRequired(), Length(min=4, max=25)])
    password_user = PasswordField('Contraseña', validators = [DataRequired(), Length(min=8)])
    passwordConfirm_user = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password_user')])
    numberPhone_user = StringField('Teléfono', validators = [DataRequired(), Length(min=10, max=10)])
    Image_user = FileField('Imagen de Usuario', validators=[ FileAllowed(['png', 'jpg'], 'Solo imágenes con extension png, jpg!')])
    submit = SubmitField('Actualizar')
