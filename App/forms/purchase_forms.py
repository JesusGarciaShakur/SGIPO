from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
#id_purchase,id_supplier,id_product,,quantity_ordered,date_ordered

class RegisterPurchaseForm(FlaskForm):
    id_supplier = SelectField('Proveedor', coerce=int, choices=[])
    id_product = SelectField('Producto', coerce=int, choices=[])
    quantity_ordered = StringField('Cantidad', validators = [DataRequired(), Length(min=1, max=3)])
    date_ordered = DateField('Fecha de solicitud', validators = [DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Registrar')

class UpdatePurchaseForm(FlaskForm):
    id_supplier = SelectField('Proveedor', coerce=int, choices=[])
    id_product = SelectField('Producto', coerce=int, choices=[])
    quantity_ordered = StringField('Cantidad', validators = [DataRequired(), Length(min=1, max=3)])
    date_ordered = DateField('Fecha de solicitud', validators = [DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Actualizar')