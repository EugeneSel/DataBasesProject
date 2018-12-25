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


class DeleteExcelDataForm(FlaskForm):
    data_list = RadioField("List of data in current file", coerce=int)

    delete = SubmitField("Delete")


class ExcelDataForm(FlaskForm):
    cell_address = StringField("Cell Address", [validators.DataRequired("Please, enter cell address."),
                                         validators.Length(2, 8, "Cell address consists of minimum 2 symbols, maximum - 8")])

    cell_data = StringField("Cell Data", [validators.DataRequired("Please, enter the data you need."),
                                         validators.Length(1, 50, "Cell data consists of minimum 1 symbols, maximum - 50")])

    cell_type = RadioField("Cell Type", [validators.InputRequired("Please, select the type of data you need.")], choices=[('Integer', 'Integer'),
                                                                                                                        ('Float', 'Float'),
                                                                                                                        ('Boolean', 'Boolean'),
                                                                                                                        ('Date', 'Date'),
                                                                                                                        ('Time', 'Time'),
                                                                                                                        ('String', 'String')])

    add = SubmitField("Add")

    update = SubmitField("Update")


class FilterExcelDataForm(FlaskForm):
    f_cell_address = StringField("Cell Address", [validators.DataRequired("Please, enter cell address."),
                                         validators.Length(2, 8, "Cell address consists of minimum 2 symbols, maximum - 8")])

    find = SubmitField("Find")

