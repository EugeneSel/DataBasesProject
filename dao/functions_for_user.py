import cx_Oracle
from dao.connection_info import *


def getUserLogin(user_login):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    user = cursor.callfunc("OUTPUT_FOR_USER.GET_USER", cx_Oracle.STRING, [user_login])

    cursor.close()
    connection.close()

    return user


def regUser(USER_LOGIN, USER_PASSWORD, USER_EMAIL):

    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    cursor.callproc("USER_AUTHORIZATION.REGISTRATION", [USER_LOGIN, USER_PASSWORD, USER_EMAIL])
    cursor.close()
    connection.close()

    return USER_LOGIN


def getUserList():
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM "User"'
    cursor.execute(query)
    result = cursor.fetchall()
    # current_user_login = cursor.callfunc("OUTPUT_FOR_USER.GET_USER_LIST", cx_Oracle.STRING, ["USER_LOGIN"])
    # cursor.execute(current_user_login)
    # result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getExcelFileName(file_name):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    excel = cursor.callfunc("OUTPUT_FOR_USER.GET_EXCEL_FILE", cx_Oracle.STRING, [file_name])

    cursor.close()
    connection.close()

    return excel


def getExcelFileList(user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = "SELECT * FROM \"Excel file\" Where user_login_fk = '%s'" %user_login
    cursor.execute(query)
    result = cursor.fetchall()
    # current_user_login = cursor.callfunc("OUTPUT_FOR_USER.GET_USER_LIST", cx_Oracle.STRING, ["USER_LOGIN"])
    # cursor.execute(current_user_login)
    # result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getDatabaseName(db_name):
    connection = cx_Oracle.connect(username, password, databaseName)
    cursor = connection.cursor()

    database = cursor.callfunc("OUTPUT_FOR_USER.GET_DB", cx_Oracle.STRING, [db_name])

    cursor.close()
    connection.close()

    return database


def getDatabaseList(user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM Database Where user_login_fk = \'%s\'' % user_login
    cursor.execute(query)
    result = cursor.fetchall()
    # current_user_login = cursor.callfunc("OUTPUT_FOR_USER.GET_USER_LIST", cx_Oracle.STRING, ["USER_LOGIN"])
    # cursor.execute(current_user_login)
    # result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getGeneratedDatabaseList(user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM "Database generation" Where user_login_fk = \'%s\'' % user_login
    cursor.execute(query)
    result = cursor.fetchall()
    # current_user_login = cursor.callfunc("OUTPUT_FOR_USER.GET_USER_LIST", cx_Oracle.STRING, ["USER_LOGIN"])
    # cursor.execute(current_user_login)
    # result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def getDataList(file_name, user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM Rule WHERE excel_file_name_fk = \'%s\' and user_login_fk = \'%s\'' % (file_name, user_login)
    cursor.execute(query)
    result = cursor.fetchall()
    # current_user_login = cursor.callfunc("OUTPUT_FOR_USER.GET_USER_LIST", cx_Oracle.STRING, ["USER_LOGIN"])
    # cursor.execute(current_user_login)
    # result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def addExcelFile(file_name, user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    cursor.callproc("WORK_WITH_EXCEL_FILE.ADD_FILE", [file_name, user_login])

    cursor.close()
    connection.close()

    return file_name


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

    cursor.callproc("WORK_WITH_DB.ADD_DB", [db_name, user_login])

    cursor.close()
    connection.close()

    return db_name


def deleteDatabase(db_name, user_login):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    cursor.callproc("WORK_WITH_DB.DELETE_DB", [db_name, user_login])

    cursor.close()
    connection.close()

    return db_name


def updateData(file_name, cell, new_data):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    message = cursor.callfunc("WORK_WITH_EXCEL_FILE.UPDATE_DATA", cx_Oracle.STRING, [file_name, cell, new_data])

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

    cursor.callproc("DB_GENERATION.CHOOSE_DATA", [file_name, user_login, cell_address, db_name])

    cursor.close()
    connection.close()

    return file_name, db_name


def createDatabase(db_name):
    connection = cx_Oracle.connect(username, password, databaseName)

    cursor = connection.cursor()

    query = 'SELECT * FROM "Database generation" WHERE new_database_name = %s' % db_name
    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result