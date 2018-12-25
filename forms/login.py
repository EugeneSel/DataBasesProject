from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class LoginForm(FlaskForm):
    login = StringField('User`s Login', validators=[validators.DataRequired('Please, enter your login: '), validators.Length(4, 20, 'Login consists of minimum 4 symbols, maximum - 20'),
                                                    validators.Regexp(r'[A-Za-z0-9_]{1,}',
                                                                      message='You entered a wrong login. Login should consist of latin letters and numbers. Please, repeat entering.')])
    password = PasswordField('User`s Password', validators=[validators.DataRequired('Please, enter your password:'), validators.Length(8, 20, 'Password consists of minimum 8 symbols, maximum - 20'),
                                                            validators.Regexp(r'[A-Za-z0-9]{1,}',
                                                                              message='You entered a wrong password. Password should consist of latin letters and numbers. Please, repeat entering.')])

    submit = SubmitField('Sign in')
