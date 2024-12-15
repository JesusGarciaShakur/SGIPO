#id_repair, objectName_repair, quantity_repaired, cost_repair, date_repair
from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class RegisterRepairForm(FlaskForm):
    objectName_repair = StringField('Nombre del objeto', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])
    quantity_repaired = StringField('Cantidad reparada', validators = [DataRequired(message="Campo requerido"), Length(min=1, max=3)])
    cost_repair = StringField('Costo de reparación', validators = [DataRequired(message="Campo requerido"), Length(min=2, max=35)])
    date_repair = DateField('Fecha de reparación', validators = [DataRequired(message="Campo requerido")], format='%Y-%m-%d')
    submit = SubmitField('Registrar')