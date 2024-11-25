from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
#id_service, name_service, description_service
class RegisterServiceForm(FlaskForm):
    name_service = StringField('Nombre del servicio', validators = [DataRequired(), Length(min=4, max=25)])
    description_service = TextAreaField('Descripción del servicio', validators = [DataRequired(), Length(min=4, max=255)])
    submit = SubmitField('Registrar')

class UpdateServiceForm(FlaskForm):
    name_service = StringField('Nombre del servicio', validators = [DataRequired(), Length(min=4, max=25)])
    description_service = TextAreaField('Descripción del servicio', validators = [DataRequired(), Length(min=4, max=255)])
    submit = SubmitField('Actualizar')