from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length

#id_return,id_sale,reason,date_return
class RegisterReturnForm(FlaskForm):
    id_sale = SelectField('Venta', coerce=int, choices=[])
    reason = TextAreaField('Motivo', validators = [DataRequired(), Length(min=1, max=250)])
    date_return = DateField('Fecha de devolución', validators = [DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Registrar')

class UpdateReturnForm(FlaskForm):
    id_sale = SelectField('Venta', coerce=int, choices=[])
    reason = TextAreaField('Motivo', validators = [DataRequired(), Length(min=1, max=250)])
    date_return = DateField('Fecha de devolución', validators = [DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Actualizar')