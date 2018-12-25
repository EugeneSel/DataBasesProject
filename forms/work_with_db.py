from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, BooleanField
from wtforms import validators


class DeleteDBForm(FlaskForm):
    db_list = RadioField("List of Your Databases", coerce=int)

    show_data = SubmitField("Show data")

    delete = SubmitField("Delete")


class AddDBForm(FlaskForm):
    db_name = StringField("New Database name", [
                                                validators.DataRequired("Please, enter Database name."),
                                                validators.Regexp(r'(?:[A-Za-z]\:\\|\\)([A-Za-z0-9\-_]\\|[A-Za-z0-9\-_]){1,}[A-Za-z0-9\-_]$',
                                                                  message="You entered invalid Database path.")])

    add = SubmitField("Add")


class GenerateDBForm(FlaskForm):
    new_db_name = StringField("New Database name", [
                                                validators.DataRequired("Please, enter Database name."),
                                                validators.Regexp(r'(?:[A-Za-z]\:\\|\\)([A-Za-z0-9\-_]\\|[A-Za-z0-9\-_]){1,}[A-Za-z0-9\-_]$',
                                                                  message="You entered invalid Database path.")])

    create = SubmitField("Create Database")
