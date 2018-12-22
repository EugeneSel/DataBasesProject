from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms import validators


class RegForm(FlaskForm):
    login = StringField("User`s Login", [validators.DataRequired("Please, enter your login."),
                                         validators.Length(4, 20, "Login consists of minimum 4 symbols, maximum - 20")])

    email = StringField("User`s email", [validators.Email("Your email is incorrect.")])

    password = PasswordField("User`s Password", [validators.DataRequired("Please, enter your password."),
                                                 validators.Length(8, 20, "Password consists of minimum 8 symbols, maximum - 20")])

    submit = SubmitField("Sign on")
