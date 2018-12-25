from flask import Flask, render_template, request, flash, session, url_for, redirect, make_response
from forms.registration import RegForm
from forms.login import LoginForm
from forms.work_with_excel_file import FilterExcelDataForm, DeleteExcelDataForm, ExcelDataForm, ChooseExcelForm, AddExcelForm
from forms.work_with_db import AddDBForm, DeleteDBForm, GenerateDBForm
from forms.work_with_user import UpdateUserForm, AddUserForm
from dao.functions_for_user import *
from datetime import datetime, timedelta
import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json


app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/')
def index():
    if 'login' in session:
        login = session['login']
        if login is None:
            return "<div>You are not logged in <br><a href = '/login'></b>" + "Click here to log in</b></a><br>" + \
                    "<a href='/registration'></b>Or here to create an account</b></a></div>"
        else:
            session['role'] = getUserList(login)[0][1]
            role = session['role']
            return render_template('index.html', login=login, role=role)
    else:
        login = request.cookies.get('login')
        session['login'] = login
        if login is None:
            return "<div>You are not logged in <br><a href = '/login'></b>" + "Click here to log in</b></a><br>" + \
                    "<a href='/registration'></b>Or here to create an account</b></a></div>"
        else:
            session['role'] = getUserList(login)[0][1]
            role = session['role']
            return render_template('index.html', login=login, role=role)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    userList = getUserList()

    if request.method == 'POST':
        is_exist = False
        correct_pass = False
        for user in userList:
            if user[0] == request.form['login']:
                is_exist = True
                if user[2] == request.form['password']:
                    correct_pass = True
                    break

        if not is_exist:
            return render_template('login.html', form=login_form, message='User with current login does not exists.')
        elif not correct_pass:
            return render_template('login.html', form=login_form, message='You entered wrong passsword. Forgot your password? Try to remember!!!')
        else:
            if login_form.validate():
                session['login'] = request.form['login']
                response = make_response(redirect(url_for('index')))
                expires = datetime.now()
                expires += timedelta(weeks=10)
                response.set_cookie('login', request.form['login'], expires=expires)
                return response
            else:
                return render_template('login.html', form=login_form)
    else:
        if 'login' in session:
            return render_template('login.html', form=login_form)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return render_template('login.html', form=login_form)
            else:
                return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    reg_form = RegForm()

    userList = getUserList()
    if request.method == 'POST':
        if not reg_form.validate():
            return render_template('registration.html', form=reg_form)
        else:
            is_unique = True
            for user in userList:
                if user[0] == request.form['login']:
                    is_unique = False
                    break

            if not is_unique:
                return render_template('registration.html', form=reg_form, is_unique='User with current login already exists.')
            else:
                user_login, message = regUser(
                    request.form['login'],
                    request.form['password'],
                    request.form['email']
                )

                if message != 'Operation successful':
                    return render_template('registration.html', form=reg_form, message=message)

                session['login'] = user_login
                response = make_response(redirect(url_for('index')))
                expires = datetime.now()
                expires += timedelta(weeks=10)
                response.set_cookie('login', user_login, expires=expires)
                return response

    return render_template('registration.html', form=reg_form)


@app.route('/ChooseExcelFile', methods=['GET', 'POST'])
def choose_excel_file():
    if 'role' not in session or session['role'] == 'Banned':
        return redirect(url_for('index'))

    login = session['login']
    fileList = getExcelFileList(login)

    add_form = AddExcelForm()
    choose_form = ChooseExcelForm()
    choose_form.file_list.choices = [(int(fileList.index(current)), current[0]) for current in fileList]
    if request.method == 'POST':
        if add_form.add.data:
            if not add_form.validate():
                return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form,
                                       login=login)
            else:
                is_unique = True
                for file in fileList:
                    if file[0] == request.form['file_name']:
                        is_unique = False
                        break

                if is_unique:
                    message = addExcelFile(request.form['file_name'], session['login'])
                    fileList = getExcelFileList(session['login'])
                    choose_form.file_list.choices = [(int(fileList.index(current)), current[0]) for current in fileList]
                    return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form,
                                           login=login, add_message=message)
                else:
                    return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form,
                                           login=login, add_message="Excel file with current name already exists.")
        elif choose_form.update.data or choose_form.delete.data:
            if not choose_form.validate():
                return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form, login=login, del_message='You didn`t choose any file.')
            else:
                if choose_form.update.data:
                    file_name = fileList[int(request.form['file_list'])][0]
                    session['file_name'] = file_name
                    return redirect(url_for('excel_file'))
                elif choose_form.delete.data:
                    file_name = fileList[int(request.form['file_list'])][0]
                    file_name = deleteExcelFile(file_name, session['login'])
                    fileList = getExcelFileList(session['login'])
                    choose_form.file_list.choices = [(int(fileList.index(current)), current[0]) for current in fileList]
                    return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form, login=login,
                                           del_message="%s file successfully deleted" % file_name)
    else:
        if 'login' in session:
            if login is None:
                return redirect(url_for('index'))
            return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form, login=login)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return redirect(url_for('index'))
            else:
                return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form, login=login)


@app.route('/ExcelEditor', methods=['GET', 'POST'])
def excel_file():
    if 'role' not in session or session['role'] == 'Banned':
        return redirect(url_for('index'))

    delete_form = DeleteExcelDataForm()
    update_form = ExcelDataForm()
    filter_form = FilterExcelDataForm()
    login = session['login']

    if session['file_name'] is None:
        return redirect(url_for('choose_excel_file'))

    file_name = session['file_name']
    dataList = getRuleList(login, file_name)
    delete_form.data_list.choices = [(int(dataList.index(current)), current[2:]) for current in dataList]
    if request.method == 'POST':
        if delete_form.delete.data:
            if not delete_form.validate():
                return render_template('excel_file.html', update_form=update_form, delete_form=delete_form, filter_form=filter_form,
                                       login=login, data=dataList, file_name=file_name, del_message='You didn`t choose any cell.')
            else:
                print(dataList[int(request.form['data_list'])][2])
                message = deleteData(
                    file_name,
                    dataList[int(request.form['data_list'])][2]
                )
                dataList = getRuleList(login, file_name)
                delete_form.data_list.choices = [(int(dataList.index(current)), current[2:]) for current in dataList]
                return render_template('excel_file.html', update_form=update_form, delete_form=delete_form, filter_form=filter_form,
                                       login=login, del_message=message, data=dataList, file_name=file_name)
        elif update_form.add.data or update_form.update.data:
            if not update_form.validate():
                return render_template('excel_file.html', update_form=update_form, delete_form=delete_form, filter_form=filter_form,
                                       login=login, data=dataList, file_name=file_name)
            else:
                if update_form.update.data:
                    message = updateData(
                        file_name,
                        request.form['cell_address'],
                        request.form['cell_data'],
                        request.form['cell_type']
                    )
                elif update_form.add.data:
                    message = addData(
                        file_name,
                        request.form['cell_address'],
                        request.form['cell_data'],
                        request.form['cell_type']
                    )
                dataList = getRuleList(login, file_name)
                delete_form.data_list.choices = [(int(dataList.index(current)), current[2:]) for current in dataList]
                return render_template('excel_file.html', update_form=update_form, delete_form=delete_form, filter_form=filter_form, login=login,
                                       update_message=message, data=dataList, file_name=file_name)
        elif filter_form.find.data:
            if not filter_form.validate():
                return render_template('excel_file.html', update_form=update_form, delete_form=delete_form, filter_form=filter_form,
                                       login=login, data=dataList, file_name=file_name)
            else:
                dataList = getRuleList(login, file_name, request.form['f_cell_address'])
                if not dataList:
                    dataList = getRuleList(login, file_name)
                    delete_form.data_list.choices = [(int(dataList.index(current)), current[2:]) for current in dataList]
                    return render_template('excel_file.html', update_form=update_form, delete_form=delete_form,
                                           filter_form=filter_form, login=login, data=dataList, file_name=file_name,
                                           filter_message='Can`t find non-empty cell %s in current file.' % request.form['f_cell_address'])
                delete_form.data_list.choices = [(int(dataList.index(current)), current[2:]) for current in dataList]
                return render_template('excel_file.html', update_form=update_form, delete_form=delete_form,
                                       filter_form=filter_form, login=login, data=dataList, file_name=file_name,
                                       filter_message='Cell %s found successfully.' % request.form['f_cell_address'])
    else:
        if 'login' in session:
            if login is None:
                return redirect(url_for('index'))
            return render_template('excel_file.html', update_form=update_form, delete_form=delete_form, filter_form=filter_form, login=login,
                                   data=dataList, file_name=file_name)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return redirect(url_for('index'))
            else:
                return render_template('excel_file.html', update_form=update_form, delete_form=delete_form, filter_form=filter_form, login=login,
                                       data=dataList, file_name=file_name)


@app.route('/Databases', methods=['GET', 'POST'])
def databases():
    if 'role' not in session or session['role'] == 'Banned':
        return redirect(url_for('index'))

    login = session['login']
    dbList = getDatabaseList(login)

    add_form = AddDBForm()
    delete_form = DeleteDBForm()
    delete_form.db_list.choices = [(int(dbList.index(current)), current[0]) for current in dbList]
    if request.method == 'POST':
        if add_form.add.data:
            if not add_form.validate():
                return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                       login=login, add_message='Please, enter Database name.')
            else:
                is_unique = True
                for db in dbList:
                    if db[0] == request.form['db_name']:
                        is_unique = False
                        break

                if is_unique:
                    message = addDatabase(request.form['db_name'], session['login'])
                    dbList = getDatabaseList(session['login'])
                    delete_form.db_list.choices = [(int(dbList.index(current)), current[0]) for current in dbList]
                    return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                           login=login, add_message=message, db_name='')
                else:
                    return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                           login=login, add_message="Database with current name already exists.")
        elif delete_form.delete.data or delete_form.show_data.data:
            if not delete_form.validate():
                return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                       login=login, del_message='Please, choose the Database.')
            else:
                if delete_form.show_data.data:
                    db_name = dbList[int(request.form['db_list'])][0]
                    new_db_list = getDBDataList(login, db_name)
                    data_list = []
                    for i in range(len(new_db_list)):
                        print(getRuleList(login, new_db_list[i][2], new_db_list[i][4]))
                        data_list.append(getRuleList(login, new_db_list[i][2], new_db_list[i][4])[0])
                    if not data_list:
                        data_list.append('This Database is empty')
                    return render_template('database.html', add_form=add_form, delete_form=delete_form, login=login,
                                           data_list=data_list, db_name=db_name)
                elif delete_form.delete.data:
                    db_name = dbList[int(request.form['db_list'])][0]
                    db_name = deleteDatabase(db_name, session['login'])
                    dbList = getDatabaseList(session['login'])
                    delete_form.db_list.choices = [(int(dbList.index(current)), current[0]) for current in dbList]
                    return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                           login=login, del_message="%s Database successfully deleted" % db_name)
    else:
        if 'login' in session:
            if login is None:
                return redirect(url_for('index'))
            return render_template('database.html', add_form=add_form, delete_form=delete_form, login=login)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return redirect(url_for('index'))
            else:
                return render_template('database.html', add_form=add_form, delete_form=delete_form, login=login)


@app.route('/Users', methods=['GET', 'POST'])
def users():
    if 'role' not in session or session['role'] != 'Admin':
        return redirect(url_for('index'))

    update_form = UpdateUserForm()
    add_form = AddUserForm()

    userList = getUserList()
    login = session['login']
    update_form.user_list.choices = [(int(userList.index(current)), current) for current in userList]
    if request.method == 'POST':
        if update_form.change_role.data or update_form.delete.data:
            if not update_form.validate():
                return render_template('user.html', update_form=update_form, add_form=add_form, login=login, update_message='You didn`t choose any User.')
            else:
                if update_form.change_role.data:
                    user_login = userList[int(request.form['user_list'])][0]
                    user_role = getUserList(user_login)[0][1]
                    if user_role == 'Admin':
                        return render_template('user.html', update_form=update_form, add_form=add_form, login=login, update_message='You can`t change role of current User')
                    user_login = updateUser(user_login)
                    userList = getUserList()
                    update_form.user_list.choices = [(int(userList.index(current)), current) for current in userList]
                    return render_template('user.html', update_form=update_form, add_form=add_form, login=login,
                                           update_message='Role of User %s updated successfully' %user_login)
                elif update_form.delete.data:
                    user_login = userList[int(request.form['user_list'])][0]
                    user_role = getUserList(user_login)[0][1]
                    if user_role == 'Admin':
                        return render_template('user.html', update_form=update_form, add_form=add_form, login=login, update_message='You can`t delete current User')
                    user_login = deleteUser(user_login)
                    userList = getUserList()
                    update_form.user_list.choices = [(int(userList.index(current)), current) for current in userList]
                    return render_template('user.html', update_form=update_form, add_form=add_form, login=login,
                                           update_message='User %s deleted successfully' % user_login)
        elif add_form.add.data:
            if not add_form.validate():
                return render_template('user.html', update_form=update_form, add_form=add_form, login=login)
            else:
                is_unique = True
                for user in userList:
                    if user[0] == request.form['login']:
                        is_unique = False
                        break

                if not is_unique:
                    return render_template('user.html', update_form=update_form, add_form=add_form, login=login,
                                           is_unique='User with current login already exists.')

                user_login, add_message = regUser(
                    request.form['login'],
                    request.form['password'],
                    request.form['email'],
                    request.form['role']
                )

                if add_message != 'Operation successful':
                    return render_template('user.html', update_form=update_form, add_form=add_form, login=login, add_message=add_message)

                userList = getUserList()
                update_form.user_list.choices = [(int(userList.index(current)), current) for current in userList]
                return render_template('user.html', update_form=update_form, add_form=add_form, login=login, add_message=add_message + ". User %s created." %user_login)
    else:
        if 'login' in session:
            if login is None:
                return redirect(url_for('index'))
            return render_template('user.html', update_form=update_form, add_form=add_form, login=login)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return redirect(url_for('index'))
            else:
                return render_template('user.html', update_form=update_form, add_form=add_form, login=login)


@app.route('/ChooseFileForNewDatabase', methods=['GET', 'POST'])
def choose_file_for_db():
    if 'role' not in session or session['role'] == 'Banned':
        return redirect(url_for('index'))

    login = session['login']
    fileList = getExcelFileList(login)

    choose_form = ChooseExcelForm()
    choose_form.file_list.choices = [(int(fileList.index(current)), current[0]) for current in fileList]
    if request.method == 'POST':
        if not choose_form.validate():
            return render_template('choose_file_for_db.html', choose_form=choose_form,
                                   login=login, choose_message='Please, choose an Excel file.')
        else:
            file_name = fileList[int(request.form['file_list'])][0]
            session['file_name'] = file_name
            return redirect(url_for('database_generation'))
    else:
        if 'login' in session:
            if login is None:
                return redirect(url_for('index'))
            return render_template('choose_file_for_db.html', choose_form=choose_form, login=login)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return redirect(url_for('index'))
            else:
                return render_template('choose_file_for_db.html', choose_form=choose_form, login=login)


@app.route('/DatabaseGeneration', methods=['GET', 'POST'])
def database_generation():
    if 'role' not in session or session['role'] == 'Banned':
        return redirect(url_for('index'))

    login = session['login']

    if session['file_name'] is None:
        return redirect(url_for('choose_file_for_db'))

    file_name = session['file_name']
    dataList = getRuleList(login, file_name)
    databaseList = getDatabaseList(login)
    newDatabaseList = getDBDataList(login)

    gen_form = GenerateDBForm()
    if request.method == 'POST':
        chosenDataList = []
        if not gen_form.validate():
            return render_template('database_generation.html', gen_form=gen_form, login=login, file_name=file_name, databaseList=databaseList, dataList=dataList)
        else:
            is_unique = True
            for db in databaseList:
                if db[0] == request.form['new_db_name']:
                    is_unique = False
                    break
            for new_db in newDatabaseList:
                if new_db[1] == request.form['new_db_name']:
                    is_unique = False
                    break

            if is_unique:
                for current in dataList:
                    if request.form.getlist(current[2]):
                        chosenDataList.append(current)
                        file_name, message = chooseData(file_name, session['login'], current[2], request.form['new_db_name'])
                message = addDatabase(request.form['new_db_name'], session['login'])
                databaseList = getDatabaseList(login)
                return render_template('database_generation.html', gen_form=gen_form, login=login, file_name=file_name, databaseList=databaseList, dataList=dataList, gen_message=message, chosenData=chosenDataList)
            else:
                return render_template('database_generation.html', gen_form=gen_form, login=login, file_name=file_name, databaseList=databaseList, dataList=dataList,
                                       gen_message="Database with current name already exists.")
    else:
        if 'login' in session:
            if login is None:
                return redirect(url_for('index'))
            return render_template('database_generation.html', gen_form=gen_form, login=login, file_name=file_name, databaseList=databaseList, dataList=dataList)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return redirect(url_for('index'))
            else:
                return render_template('database_generation.html', gen_form=gen_form, login=login, file_name=file_name, databaseList=databaseList, dataList=dataList)


@app.route('/Statistics', methods=['GET'])
def plots():
    if 'role' not in session or session['role'] == 'Banned':
        return redirect(url_for('index'))

    login = session['login']
    if 'login' in session:
        if login is None:
            return redirect(url_for('index'))

        fileList = getAllExcelFileList(login)
        dbList = getAllDatabaseList(login)
        countList = countExcelDataList(login)

        traceExcel = go.Scatter(
            x=[current[3] for current in fileList],
            y=[current[0] for current in fileList],
            name='Excel files'
        )

        traceDB = go.Scatter(
            x=[current[3] for current in dbList],
            y=[current[0] for current in dbList],
            name='Databases'
        )

        countExcelData = go.Bar(
            x=[current[0] for current in countList],
            y=[current[1] for current in countList]
        )

        dataScatter = [traceExcel, traceDB]
        dataBar = [countExcelData]
        graphJSONscatter = json.dumps(dataScatter, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSONbar = json.dumps(dataBar, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('statistics.html', login=login,
                               graphJSONscatter=graphJSONscatter, graphJSONbar=graphJSONbar)
    else:
        login = request.cookies.get('login')
        session['login'] = login
        if login is None:
            return redirect(url_for('index'))
        else:
            fileList = getAllExcelFileList(login)
            dbList = getAllDatabaseList(login)
            countList = countExcelDataList(login)

            traceExcel = go.Scatter(
                x=[current[3] for current in fileList],
                y=[current[0] for current in fileList],
                name='Excel files'
            )

            traceDB = go.Scatter(
                x=[current[3] for current in dbList],
                y=[current[0] for current in dbList],
                name='Databases'
            )

            countExcelData = go.Bar(
                x=[current[0] for current in countList],
                y=[current[1] for current in countList]
            )

            dataScatter = [traceExcel, traceDB]
            dataBar = [countExcelData]
            graphJSONscatter = json.dumps(dataScatter, cls=plotly.utils.PlotlyJSONEncoder)
            graphJSONbar = json.dumps(dataBar, cls=plotly.utils.PlotlyJSONEncoder)
            return render_template('statistics.html', login=login,
                                   graphJSONscatter=graphJSONscatter, graphJSONbar=graphJSONbar)


@app.route('/logout')
def logout():
    session.pop('login', None)
    response = make_response(redirect(url_for('index')))
    response.set_cookie('login', '', expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
