# id_client, name_client, lastName_client, age_client, numberPhone_client, email_client, direction_client, id_disease
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class RegisterClientForm(FlaskForm):
    name_client = StringField('Nombre(s)', validators = [DataRequired(), Length(min=4, max=25)])
    lastName_client = StringField('Apellido(s)', validators = [DataRequired(), Length(min=4, max=25)])
    age_client = StringField('Edad', validators = [DataRequired(), Length(min=1, max=3)])
    numberPhone_client = StringField('Teléfono', validators = [DataRequired(), Length(min=10, max=10)])
    email_client = StringField('Correo Electrónico', validators = [DataRequired(), Length(min=4, max=35)])
    direction_client = StringField('Dirección', validators = [DataRequired(), Length(min=4, max=50)])
    id_disease = SelectField('Padecimiento', coerce=int, choices=[])
    submit = SubmitField('Registrar')

class UpdateClientForm(FlaskForm):
    name_client = StringField('Nombre(s)', validators = [DataRequired(), Length(min=4, max=25)])
    lastName_client = StringField('Apellido(s)', validators = [DataRequired(), Length(min=4, max=25)])
    age_client = StringField('Edad', validators = [DataRequired(), Length(min=1, max=3)])
    numberPhone_client = StringField('Teléfono', validators = [DataRequired(), Length(min=10, max=10)])
    email_client = StringField('Correo Electrónico', validators = [DataRequired(), Length(min=4, max=35)])
    direction_client = StringField('Dirección', validators = [DataRequired(), Length(min=4, max=50)])
    id_disease = SelectField('Padecimiento', coerce=int, choices=[])
    submit = SubmitField('Actualizar')