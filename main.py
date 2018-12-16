from flask import Flask, render_template, request, flash, session, url_for, redirect, make_response
from forms.registration import RegForm
from forms.login import LoginForm
from forms.work_with_excel_file import ExcelForm, ChooseExcelForm, AddExcelForm
from forms.work_with_db import AddDBForm, DeleteDBForm, GenerateDBForm
from dao.functions_for_user import *
from datetime import datetime, timedelta
import numpy as np


app = Flask(__name__)
app.secret_key = 'development key'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' or request.method == 'GET':
        if 'login' in session:
            login = session['login']
            if login is None:
                return "<div>You are not logged in <br><a href = '/login'></b>" + "Click here to log in</b></a><br>" + \
                        "<a href='/registration'></b>Or here to create an account</b></a></div>"
            return render_template('index.html', login=login)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return "<div>You are not logged in <br><a href = '/login'></b>" + "Click here to log in</b></a><br>" + \
                        "<a href='/registration'></b>Or here to create an account</b></a></div>"
            else:
                return render_template('index.html', login=login)


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
        session['login'] = request.form['login']
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
                user_login = regUser(
                    request.form['login'],
                    request.form['password'],
                    request.form['email']
                )

                session['login'] = user_login
                response = make_response(redirect(url_for('index')))
                expires = datetime.now()
                expires += timedelta(weeks=10)
                response.set_cookie('login', user_login, expires=expires)
                return response

    return render_template('registration.html', form=reg_form)


@app.route('/Databases', methods=['GET', 'POST'])
def databases():
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
                    db_name = addDatabase(request.form['db_name'], session['login'])
                    dbList = getDatabaseList(session['login'])
                    delete_form.db_list.choices = [(int(dbList.index(current)), current[0]) for current in dbList]
                    return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                           login=login,
                                           add_message="%s Database successfully created." % db_name)
                else:
                    return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                           login=login,
                                           add_message="Database with current name already exists.")
        elif delete_form.delete.data:
            if not delete_form.validate():
                return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                       login=login, del_message='Please, choose the Database.')
            else:
                db_name = dbList[int(request.form['db_list'])][0]
                db_name = deleteDatabase(db_name, session['login'])
                dbList = getDatabaseList(session['login'])
                delete_form.db_list.choices = [(int(dbList.index(current)), current[0]) for current in dbList]
                return render_template('database.html', add_form=add_form, delete_form=delete_form,
                                       login=login,
                                       del_message="%s Database successfully deleted" % db_name)
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


@app.route('/ChooseFileForNewDatabase', methods=['GET', 'POST'])
def choose_file_for_db():
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
    login = session['login']
    file_name = session['file_name']
    dataList = getDataList(file_name, login)
    databaseList = getDatabaseList(login)
    newDatabaseList = getGeneratedDatabaseList(login)


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
                    print(current)
                    if request.form.getlist(current[2]):
                        chosenDataList.append(current)
                        print(chosenDataList)
                        file_name, new_db_name = chooseData(file_name, session['login'], current[2], request.form['new_db_name'])
                new_db_name = addDatabase(request.form['new_db_name'], session['login'])
                databaseList = getDatabaseList(login)
                return render_template('database_generation.html', gen_form=gen_form, login=login, file_name=file_name, databaseList=databaseList, dataList=dataList, gen_message='%s generated successfully and includes such data:' % new_db_name, chosenData=chosenDataList)
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


@app.route('/ChooseExcelFile', methods=['GET', 'POST'])
def choose_excel_file():
    login = session['login']
    fileList = getExcelFileList(login)

    add_form = AddExcelForm()
    choose_form = ChooseExcelForm()
    choose_form.file_list.choices = [(int(fileList.index(current)), current[0]) for current in fileList]
    if request.method == 'POST':
        if add_form.add.data:
            if not add_form.validate():
                return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form,
                                       login=login, add_message='Please, enter file name')
            else:
                is_unique = True
                for file in fileList:
                    if file[0] == request.form['file_name']:
                        is_unique = False
                        break

                if is_unique:
                    file_name = addExcelFile(request.form['file_name'], session['login'])
                    fileList = getExcelFileList(session['login'])
                    choose_form.file_list.choices = [(int(fileList.index(current)), current[0]) for current in fileList]
                    return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form,
                                           login=login,
                                           add_message="%s file successfully created" % file_name)
                else:
                    return render_template('choose_excel_file.html', add_form=add_form, choose_form=choose_form,
                                           login=login,
                                           add_message="Excel file with current name already exists.")
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
    excel_form = ExcelForm()

    login = session['login']
    file_name = session['file_name']
    dataList = getDataList(file_name, login)
    if request.method == 'POST':
        if not excel_form.validate():
            return render_template('excel_file.html', form=excel_form, login=login, data=dataList, file_name=file_name)
        else:
            if excel_form.update.data:
                message = updateData(
                file_name,
                request.form['cell_address'],
                request.form['cell_data']
            )
            elif excel_form.add.data:
                message = addData(
                file_name,
                request.form['cell_address'],
                request.form['cell_data'],
                request.form['cell_type']
            )
            elif excel_form.delete.data:
                message = deleteData(
                file_name,
                request.form['cell_address']
            )
            dataList = getDataList(file_name, login)
            return render_template('excel_file.html', form=excel_form, login=login,
                                    message=message, data=dataList, file_name=file_name)
    else:
        if 'login' in session:
            if login is None:
                return redirect(url_for('index'))
            return render_template('excel_file.html', form=excel_form, login=login, data=dataList, file_name=file_name)
        else:
            login = request.cookies.get('login')
            session['login'] = login
            if login is None:
                return redirect(url_for('index'))
            else:
                return render_template('excel_file.html', form=excel_form, login=login, is_exist='', data=dataList, file_name=file_name)


@app.route('/logout')
def logout():
    session.pop('login', None)
    response = make_response(redirect(url_for('index')))
    response.set_cookie('login', '', expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
