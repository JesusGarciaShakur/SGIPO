from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

#id_brand,name_brand ,description_brand ,id_supplier
class RegisterBrandForm(FlaskForm):
    name_brand = StringField('Nombre de la marca', validators = [DataRequired(), Length(min=4, max=50)])
    description_brand = TextAreaField('Descripción de la marca', validators = [DataRequired(), Length(min=4, max=250)])
    id_supplier = SelectField('Proveedor', coerce=int, choices = [])
    submit = SubmitField('Registrar')

class  UpdateBrandForm(FlaskForm):
    name_brand = StringField('Nombre de la marca', validators = [DataRequired(), Length(min=4, max=50)])
    description_brand = TextAreaField('Descripción de la marca', validators = [DataRequired(), Length(min=4, max=250)])
    id_supplier = SelectField('Proveedor', coerce=int, choices = [])
    submit = SubmitField('Actualizar')