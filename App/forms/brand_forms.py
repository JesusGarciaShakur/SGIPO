from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField

#id_brand,name_brand ,description_brand ,id_supplier
class RegisterBrandForm(FlaskForm):
    name_brand = StringField('Nombre de la marca', validators = [DataRequired(), Length(min=4, max=50)])
    description_brand = TextAreaField('Descripción de la marca', validators = [DataRequired(), Length(min=4, max=250)])
    id_supplier = SelectField('Proveedor', coerce=int, choices = [])
    image_brand = FileField('Imagen de marca', validators=[ FileAllowed(['png', 'jpg'], 'Solo imágenes con extension png, jpg!')])
    submit = SubmitField('Registrar')

class  UpdateBrandForm(FlaskForm):
    name_brand = StringField('Nombre de la marca', validators = [DataRequired(), Length(min=4, max=50)])
    description_brand = TextAreaField('Descripción de la marca', validators = [DataRequired(), Length(min=4, max=250)])
    id_supplier = SelectField('Proveedor', coerce=int, choices = [])
    image_brand = FileField('Imagen de marca', validators=[ FileAllowed(['png', 'jpg'], 'Solo imágenes con extension png, jpg!')])
    submit = SubmitField('Actualizar')