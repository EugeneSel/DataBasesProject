from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class LoginForm(FlaskForm):
    login = StringField('User`s Login', validators=[validators.DataRequired('Please, enter your login: '), validators.Length(4, 20, 'Login consists of minimum 4 symbols, maximum - 20')])
    password = PasswordField('User`s Password', validators=[validators.DataRequired('Please, enter your password:'), validators.Length(8, 20, 'Password consists of minimum 8 symbols, maximum - 20')])

    submit = SubmitField('Sign in')
