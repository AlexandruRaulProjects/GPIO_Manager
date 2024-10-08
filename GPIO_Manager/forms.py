from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Flask_GPIO_Manager.GPIO_Manager.model import User


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(),
                               Length(min=2, max=20)
                           ])
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired()
                             ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         DataRequired(),
                                         EqualTo('password')
                                     ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query \
            .filter_by(username=username.data) \
            .first()

        if user:
            raise ValidationError('That username is taken. Please Choose a different one! ')

    def validate_email(self, email):

        user = User \
            .query \
            .filter_by(username=email.data).first()

        if user:
            raise ValidationError('That email is taken. Please Choose a different one! ')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(),
                            Email()
                        ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired()
                             ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddPinForm(FlaskForm):
    name = SelectField('Pin Name',
                       choices=[
                           'Pin 1',
                           'Pin 2'
                       ])
    number = StringField('Pin Number',
                         validators=[
                             DataRequired(),
                             Length(min=1, max=2)
                         ])
    submit = SubmitField('Add')
