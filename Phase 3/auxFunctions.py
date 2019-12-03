import pandas as pd
import pymysql
import mydbconfig as mydb
from app import app


def get_connection():
    """Return a connection object to project database at magenta.mysitehosted.com on success.

    :return:    On success, tuple (True, <connection object>).
                On failure, tuple (False, <error message>).

    Note: It is up to the user to close the connection when done.
    """
    # todo don't forget to close connection when done
    try:
        conn = pymysql.connect(mydb.DB_HOST, mydb.DB_USER, mydb.DB_PASSWORD, mydb.DB_DB)
        return True, conn
    except pymysql.Error as exc:
        _, message = exc.args
        return False, message


def get_scalar(sql, paramList=None):
    """Return scalar result of SQL query (parallel to ExecuteScalar) on success

    :param sql: SQL query (using %s) that returns a single scalar value (e.g., SELECT COUNT(*) FROM t)
    :param paramList: List of parameters to substitute in sql for %s occurrences
    :return:    On success, tuple (True, <returned scalar value)
                On failure, tuple (False, <error message>).
    """
    conn = get_connection()
    if conn[0]:
        db = conn[1]
        try:
            cursor = db.cursor()
            cursor.execute(sql, args=paramList)
            output = cursor.fetchone()
            cursor.close()
            return True, output
        except pymysql.Error as exc:
            _, message = exc.args
            return False, message
        finally:
            if db.open:
                db.close()
    else:
        return False, conn[1]


def get_df(sql, paramList=None):
    """Return Pandas DataFrame filled with rows returned by sql query

    :param sql: SQL SELECT query (using %s)
    :param paramList: List of parameters to substitute in sql for %s occurrences
    :return:    On success, tuple (True, <DataFrame>)
                On failure, tuple (False, <error message>)
    """
    # sql is a SQL statement with %s in place of parameters to be substituted
    # params is a list of parameters to substitute within sql
    # Example: get_df('SELECT cityName WHERE state = %s', ['CA'])
    conn = get_connection()
    if conn[0]:
        db = conn[1]
        try:
            df = pd.read_sql_query(sql, con=db, params=paramList)
            return True, df
        except pymysql.Error as exc:
            _, message = exc.args
            return False, message
        except:
            return  False, "Unexpected error!!!"
        finally:
            if db.open:
                db.close()
    else:
        return False, conn[1]


def get_table2_5(sql,param ='None'):
    db = pymysql.connect(mydb.DB_HOST, mydb.DB_USER, mydb.DB_PASSWORD, mydb.DB_DB)
    conn = db.cursor()
    if param == 'None':
        conn.execute(sql)
    else:
        conn.execute(sql,[param,param])
    table = conn.fetchall()
    conn.close()
    if db.open:
        db.close()
    return table


def get_two_tables(sql):
    """
    return tuple of two tables for Population Revenue report, one using total revenue, the other using total revenue
    :param sql: SQL for both tables of Population Revenue report
    :return:    On success, tuple (True, <total_revenue_table>, <avg_revenue_table2>)
                On failure, tuple (False, <error message>)
tuples of two tables, one using total revenue, the other using average revenue
    """
    conn = get_connection()
    if conn[0]:
        db = conn[1]
        try:
            cursor = db.cursor()
            cursor.execute(sql)
            output = cursor.fetchall()
            cursor.close()
            table1 = [(year, small, medium, large, extraLarge) for (year, small, medium, large, extraLarge, _, _, _, _)
                      in output]
            table2 = [(year, small, medium, large, extraLarge) for (year, _, _, _, _, small, medium, large, extraLarge)
                      in output]
            return True, table1, table2
        except pymysql.Error as exc:
            _, message = exc.args
            return False, message
        except:
            return False, "Unexpected error!!!"
        finally:
            if db.open:
                db.close()
    else:
        return False, conn[1]


def get_table1_5(sql, param ='None'):
    db = pymysql.connect(mydb.DB_HOST, mydb.DB_USER, mydb.DB_PASSWORD, mydb.DB_DB)
    conn = db.cursor()
    if param == 'None':
        conn.execute(sql)
    else:
        conn.execute(sql,param)
    table = conn.fetchall()
    conn.close()
    if db.open:
        db.close()
    return table


def get_table_rl(sql, paramList=None):
    """
    Return tuple representing entire table returned from sql query
    :param sql: SQL SELECT query (using %s)
    :param paramList: List of parameters to substitute in sql for %s occurrences
    :return:    On success, tuple (True, <table tuple>)
                On failure, tuple (False, <table tuple>)

    """
    conn = get_connection()
    if conn[0]:
        db = conn[1]
        try:
            cursor = db.cursor()
            cursor.execute(sql, args=paramList)
            output = cursor.fetchall()
            cursor.close()
            return True, output
        except pymysql.Error as exc:
            _, message = exc.args
            return False, message
        except:
            return False, "Unexpected error!!!"
        finally:
            if db.open:
                db.close()
    else:
        return False, conn[1]


def get_table2(sql, param ='None'):
    db = pymysql.connect(mydb.DB_HOST, mydb.DB_USER, mydb.DB_PASSWORD, mydb.DB_DB)
    # conn = db.cursor()
    if param == 'None':
        conn = db.cursor()
        conn.execute(sql)
        table = conn.fetchall()
        conn.close()
        if db.open:
            db.close()
        return table
    else:
        df = pd.read_sql_query(sql, db, params=(param, param))
        #todo update params to be any length, not just 2
        db.close()
        return df.to_html(index=False)


def get_table3(sql, param ='None'):
    db = pymysql.connect(mydb.DB_HOST, mydb.DB_USER, mydb.DB_PASSWORD, mydb.DB_DB)
    if param == 'None':
        conn = db.cursor()
        conn.execute(sql)
        table = conn.fetchall()
        conn.close()
        if db.open:
            db.close()
        return table
    else:
        df = pd.read_sql_query(sql, db, params=(param,))
        db.close()
        return df.to_html(index=False)


def get_table4(sql, param ='None'):
    #this has been created for statevol report
    # takes param and passes to SQL: month, year, month, year
    db = pymysql.connect(mydb.DB_HOST, mydb.DB_USER, mydb.DB_PASSWORD, mydb.DB_DB)
    if param == 'None':
        conn = db.cursor()
        conn.execute(sql)
        table = conn.fetchall()
        conn.close()
        if db.open:
            db.close()
        return table
    else:
        dataF = pd.read_sql_query(sql, db, params = (param[0], param[1], param[0], param[1]))
        db.close()
        return dataF


def get_table(df):
    """Return an HTML table element based on a Pandas DataFrame

    :param df: A Pandas DataFrame
    :return: HTML table (<table>...</table)
    """
    return df.to_html(index=False)


def writeQuery(sql, paramList=None):
    '''Execute SQL statement that modifies table (UPDATE, INSERT, DELETE)

    :param sql: SQL statement (using %s) such as UPDATE, INSERT, or DELETE
    :param paramList: paramList: List of parameters to substitute in sql for %s occurrences
    :return:    On success, tuple (True, <output from sql execution>)
                On failure, tuple (False, <error message>)
    '''
    conn = get_connection()
    if conn[0]:
        db = conn[1]
        try:
            cursor = db.cursor()
            cursor.execute(sql, args=paramList)
            output = db.commit()
            cursor.close()
            return True, output
        except pymysql.Error as exc:
            _, message = exc.args
            return False, message
        finally:
            if db.open:
                db.close()
    else:
        return False, conn[1]


def getSqlStatementFromFile(pathName, fileName):
    #pathName = SQL_PATH
    #fileName = '09. Display Actual vs Predicted GPS.sql'

    fd = open(pathName + "/" + fileName, 'r')
    sqlStatement = fd.read()
    fd.close()
    return sqlStatement

def getSql(fileName):
    """Return the contents of text file located in app/SQL folder as a string

    :param fileName: Name of file in app/SQL folder
    :return:    On success, tuple (True, <contents of fileName as a string>)
                On failure, tuple (False, <error message>)
    """
    SQL_PATH = app.root_path + "/sql"
    try:
        path = SQL_PATH + "/" + fileName
        with open(path, 'r') as sqlFile:
            contents = sqlFile.read()
            return True, contents
    except FileNotFoundError as fnf:
        _, message = fnf.args
        return False, message
    except IOError as io:
        _, message = io.args
        return False, message
    except:
        return False, 'Unexpected error!!!'


def getSqlSplit(fileName):
    """Return the multiple single-line SQL statements in text file located in app/SQL folder as a string array

    :param fileName: Name of file in app/SQL folder holding multiple single-line SQL statements
    :return:    On success, tuple (True, <contents of fileName as a string array>)
                On failure, tuple (False, <error message>)
    """
    ret = getSql(fileName)
    if ret[0]:
        return True, ret[1].split('\n')
    return False, ret[1]
