from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length
#id_service, name_service, description_service
class RegisterServiceForm(FlaskForm):
    name_service = StringField('Nombre del servicio', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])
    description_service = TextAreaField('Descripción del servicio', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=255)])
    submit = SubmitField('Registrar')

class UpdateServiceForm(FlaskForm):
    name_service = StringField('Nombre del servicio', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])
    description_service = TextAreaField('Descripción del servicio', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=255)])
    submit = SubmitField('Actualizar')

#id_request, id_service, id_client, date_request, price_request
class RegisterServiceRequestForm(FlaskForm):
    id_service = SelectField('Servicio', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un Servicio")])
    id_client = SelectField('Cliente', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un Cliente")])
    date_request = DateField('Fecha de solicitud de servicio', validators = [DataRequired(message="Campo requerido")], format='%Y-%m-%d')
    price_request = StringField('Precio', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])
    submit = SubmitField('Registrar')

class UpdateServiceRequestForm(FlaskForm):
    id_service = SelectField('Servicio', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un Servicio")])
    id_client = SelectField('Cliente', coerce=int, choices=[], validators=[DataRequired(message="Seleccione un Cliente")])
    date_request = DateField('Fecha de solicitud de servicio', validators = [DataRequired(message="Campo requerido")], format='%Y-%m-%d')
    price_request = StringField('Precio', validators = [DataRequired(message="Campo requerido"), Length(min=4, max=25)])
    submit = SubmitField('Actualizar')
