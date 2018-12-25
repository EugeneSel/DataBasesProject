import cx_Oracle
from dao.connection_info import *


def regUser(user_login, user_password, user_email, user_role=None):

    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()
    message = cursor.var(cx_Oracle.STRING)

    if not user_role:
        cursor.callproc("USER_AUTHORIZATION.REGISTRATION", [user_login, user_password, user_email, message])
    else:
        cursor.callproc("USER_AUTHORIZATION.REGISTRATION", [user_login, user_password, user_email, message, user_role])

    cursor.close()
    connection.close()

    return user_login, message.getvalue()


def getUserList(login=None):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    if login is None:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_USER_LIST())'
        cursor.execute(query)
    else:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_USER_LIST(:login))'
        cursor.execute(query, login=login)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getExcelFileList(user_login, file_name=None):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    if not file_name:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_EXCEL_FILE_LIST(:user_login))'
        cursor.execute(query, user_login=user_login)
    else:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_EXCEL_FILE_LIST(:user_login, :file_name))'
        cursor.execute(query, user_login=user_login, file_name=file_name)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getAllExcelFileList(user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = "Select * From \"Excel file\" Where user_login_fk = '%s'" % user_login
    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getDatabaseList(user_login, db_name=None):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    if not db_name:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_DB_LIST(:user_login))'
        cursor.execute(query, user_login=user_login)
    else:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_DB_LIST(:user_login, :db_name))'
        cursor.execute(query, user_login=user_login, db_name=db_name)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getAllDatabaseList(user_login, db_name=None):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = "Select * From Database Where user_login_fk = '%s'" % user_login
    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def countExcelDataList(user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = "Select excel_file_name_fk, count(*) From Rule Where user_login_fk = '%s' Group by excel_file_name_fk" % user_login
    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getRuleList(user_login, file_name=None, cell_address=None):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    if not file_name and not cell_address:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_RULE_LIST(:user_login))'
        cursor.execute(query, user_login=user_login)
    elif not cell_address:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_RULE_LIST(:user_login, :file_name))'
        cursor.execute(query, user_login=user_login, file_name=file_name)
    else:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_RULE_LIST(:user_login, :file_name, :cell_address))'
        cursor.execute(query, user_login=user_login, file_name=file_name, cell_address=cell_address)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getDBDataList(user_login, db_name=None):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    if not db_name:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_DBDATA_LIST(:user_login))'
        cursor.execute(query, user_login=user_login)
    else:
        query = 'SELECT * FROM table(OUTPUT_FOR_USER.GET_DBDATA_LIST(:user_login, :db_name))'
        cursor.execute(query, user_login=user_login, db_name=db_name)

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def addExcelFile(file_name, user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()
    message = cursor.var(cx_Oracle.STRING)

    cursor.callproc("WORK_WITH_EXCEL_FILE.ADD_FILE", [file_name, user_login, message])

    cursor.close()
    connection.close()

    return message.getvalue()


def deleteExcelFile(file_name, user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    cursor.callproc("WORK_WITH_EXCEL_FILE.DELETE_FILE", [file_name, user_login])

    cursor.close()
    connection.close()

    return file_name


def addDatabase(db_name, user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()
    message = cursor.var(cx_Oracle.STRING)

    cursor.callproc("WORK_WITH_DB.ADD_DB", [db_name, user_login, message])

    cursor.close()
    connection.close()

    return message.getvalue()


def deleteDatabase(db_name, user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    cursor.callproc("WORK_WITH_DB.DELETE_DB", [db_name, user_login])

    cursor.close()
    connection.close()

    return db_name


def updateUser(login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    cursor.callproc("WORK_WITH_USER.CHANGE_USER_ROLE", [login])

    cursor.close()
    connection.close()

    return login


def deleteUser(login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    cursor.callproc("WORK_WITH_USER.DELETE_USER", [login])

    cursor.close()
    connection.close()

    return login


def updateData(file_name, cell, new_data, new_data_type):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    message = cursor.callfunc("WORK_WITH_EXCEL_FILE.UPDATE_DATA", cx_Oracle.STRING, [file_name, cell, new_data, new_data_type])

    cursor.close()
    connection.close()

    return message


def deleteData(file_name, cell):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    message = cursor.callfunc("WORK_WITH_EXCEL_FILE.DELETE_DATA", cx_Oracle.STRING, [file_name, cell])

    cursor.close()
    connection.close()

    return message


def addData(file_name, cell_address, cell_data, cell_type):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    message = cursor.callfunc("WORK_WITH_EXCEL_FILE.ADD_DATA", cx_Oracle.STRING, [file_name, cell_address, cell_data, cell_type])

    cursor.close()
    connection.close()

    return message


def chooseData(file_name, user_login, cell_address, db_name):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()
    message = cursor.var(cx_Oracle.STRING)

    cursor.callproc("DB_GENERATION.CHOOSE_DATA", [file_name, user_login, cell_address, db_name, message])

    cursor.close()
    connection.close()

    return file_name, message.getvalue()


def createDatabase(db_name):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM "Database generation" WHERE new_database_name = %s' % db_name
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result