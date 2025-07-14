from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField, DateField, SelectField , IntegerField
from wtforms.validators import DataRequired, Email, Length,DataRequired

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=150)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class TaskForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    due_date = DateField('Fecha de Vencimiento', format='%Y-%m-%d', validators=[DataRequired()])
    status = SelectField('Estado', choices=[
        ('Pendiente', 'Pendiente'),
        ('En progreso', 'En progreso'),
        ('Completada', 'Completada')
    ])
    character_id = IntegerField('ID Personaje (opcional)')
    submit = SubmitField('Guardar')