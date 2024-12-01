from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

#id_supplier, name_supplier, direction_supplier ,rfc_supplier ,contact_supplier
class RegisterSupplierForm(FlaskForm):
    name_supplier = StringField('Nombre del proveedor', validators = [DataRequired(), Length(min=4, max=50)])
    direction_supplier = StringField('Dirección del proveedor', validators = [DataRequired(), Length(min=4, max=25)])
    rfc_supplier = StringField('RFC del proveedor', validators = [DataRequired(), Length(min=4, max=25)])
    contact_supplier = StringField('Contacto del proveedor', validators = [DataRequired(), Length(min=4, max=25)])
    submit = SubmitField('Registrar')

class UpdateSupplierForm(FlaskForm):
    name_supplier = StringField('Nombre del proveedor', validators = [DataRequired(), Length(min=4, max=50)])
    direction_supplier = StringField('Dirección del proveedor', validators = [DataRequired(), Length(min=4, max=25)])
    rfc_supplier = StringField('RFC del proveedor', validators = [DataRequired(), Length(min=4, max=25)])
    contact_supplier = StringField('Contacto del proveedor', validators = [DataRequired(), Length(min=4, max=25)])
    submit = SubmitField('Actualizar')