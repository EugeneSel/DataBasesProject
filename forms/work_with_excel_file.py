from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms import validators


class ChooseExcelForm(FlaskForm):
    file_list = RadioField("List of Your Excel files", coerce=int)

    update = SubmitField("Update")

    delete = SubmitField("Delete")

    choose = SubmitField("Choose Excel file")


class AddExcelForm(FlaskForm):
    file_name = StringField("New Excel file name", [validators.DataRequired("Please, enter file name.")])

    add = SubmitField("Add")


class ExcelForm(FlaskForm):
    cell_address = StringField("Cell Address", [validators.DataRequired("Please, enter cell address.")])

    cell_data = StringField("Cell Data", [validators.DataRequired("Please, enter the data you need.")])

    cell_type = StringField("Cell Type", [validators.DataRequired("Please, enter the type of data you need.")])

    add = SubmitField("Add")

    update = SubmitField("Update")

    delete = SubmitField("Delete")
