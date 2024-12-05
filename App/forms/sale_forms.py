from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

#id_sale,id_client,id_product,,quantity_sold,final_price,date_sold
class RegisterSaleForm(FlaskForm):
    id_client = SelectField('Cliente', coerce=int, choices=[])
    id_product = SelectField('Producto', coerce=int, choices=[])
    quantity_sold = StringField('Cantidad', validators = [DataRequired(), Length(min=1, max=3)])
    final_price = StringField('Precio final', validators = [DataRequired(), Length(min=1, max=5)])
    date_sold = DateField('Fecha de venta', validators = [DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Registrar')

class UpdateSaleForm(FlaskForm):
    id_client = SelectField('Cliente', coerce=int, choices=[])
    id_product = SelectField('Producto', coerce=int, choices=[])
    quantity_sold = StringField('Cantidad', validators = [DataRequired(), Length(min=1, max=3)])
    final_price = StringField('Precio final', validators = [DataRequired(), Length(min=1, max=5)])
    date_sold = DateField('Fecha de venta', validators = [DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Actualizar')