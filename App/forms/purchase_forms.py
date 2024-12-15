from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
#id_purchase,id_supplier,id_product,,quantity_ordered,date_ordered

class RegisterPurchaseForm(FlaskForm):
    id_supplier = SelectField('Proveedor', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un Distribuidor")])
    id_product = SelectField('Producto', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un Producto")])
    quantity_ordered = StringField('Cantidad', validators = [DataRequired(message="Campo requerido"), Length(min=1, max=3)])
    date_ordered = DateField('Fecha de solicitud', validators = [DataRequired(message="Campo requerido")], format='%Y-%m-%d')
    submit = SubmitField('Registrar')

class UpdatePurchaseForm(FlaskForm):
    id_supplier = SelectField('Proveedor', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un Distribuidor")])
    id_product = SelectField('Producto', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un Producto")])
    quantity_ordered = StringField('Cantidad', validators = [DataRequired(message="Campo requerido"), Length(min=1, max=3)])
    date_ordered = DateField('Fecha de solicitud', validators = [DataRequired(message="Campo requerido")], format='%Y-%m-%d')
    submit = SubmitField('Actualizar')