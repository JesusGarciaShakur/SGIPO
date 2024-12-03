from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

#id_product, name_product, description_product, id_brand, price_product, stock_product
class RegisterProductForm(FlaskForm):
    name_product = StringField('Nombre del producto', validators = [DataRequired(), Length(min=4, max=50)])
    description_product = TextAreaField('Descripción del producto', validators = [DataRequired(), Length(min=4, max=250)])
    id_brand = SelectField('Marca', coerce=int, choices=[])
    price_product = StringField('Precio', validators = [DataRequired(), Length(min=1, max=10)])
    stock_product = StringField('Stock', validators = [DataRequired(), Length(min=1, max=10)])
    submit = SubmitField('Registrar')

class UpdateProductForm(FlaskForm):
    name_product = StringField('Nombre del producto', validators = [DataRequired(), Length(min=4, max=50)])
    description_product = TextAreaField('Descripción del producto', validators = [DataRequired(), Length(min=4, max=250)])
    id_brand = SelectField('Marca', coerce=int, choices=[])
    price_product = StringField('Precio', validators = [DataRequired(), Length(min=1, max=10)])
    stock_product = StringField('Stock', validators = [DataRequired(), Length(min=1, max=10)])
    submit = SubmitField('Editar')