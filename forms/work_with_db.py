from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, BooleanField
from wtforms import validators


class DeleteDBForm(FlaskForm):
    db_list = RadioField("List of Your Databases", coerce=int)

    delete = SubmitField("Delete")


class AddDBForm(FlaskForm):
    db_name = StringField("New Database name", [validators.DataRequired("Please, enter Database name.")])

    add = SubmitField("Add")


class GenerateDBForm(FlaskForm):
    new_db_name = StringField("New Database name", [validators.DataRequired("Please, enter Database name.")])

    create = SubmitField("Create Database")
