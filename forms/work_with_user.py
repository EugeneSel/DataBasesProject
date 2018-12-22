from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, BooleanField, PasswordField
from wtforms import validators


class UpdateUserForm(FlaskForm):
    user_list = RadioField("List of Users", coerce=int)

    change_role = SubmitField("Ban/Unban")

    delete = SubmitField("Delete")


class AddUserForm(FlaskForm):
    login = StringField("User`s Login", [validators.DataRequired("Please, enter user`s login."),
                                         validators.Length(4, 20, "Login consists of minimum 4 symbols, maximum - 20")])

    email = StringField("User`s email", [validators.Email("User email is incorrect.")])

    password = PasswordField("User`s Password", [validators.DataRequired("Please, enter user`s password."),
                                                 validators.Length(8, 20,
                                                                   "Password consists of minimum 8 symbols, maximum - 20")])

    role = RadioField("User`s role", choices=[('Admin', 'Admin'), ('Default', 'Default'), ('Banned', 'Banned')])

    add = SubmitField("add")
