from flask import render_template
from app import app
import pymysql
import auxFunctions as aux
import mydbconfig


def get_statistics():
    # For speed, leave connection open for all queries before closing
    statistics = aux.getSqlSplit('01. Display Main Menu.sql')
    if not statistics[0]:
        return False, 'Unable to read SQL statements. Cannot continue!!!'
    statistics_sql = statistics[1]
    SQL_STORE_COUNT = statistics_sql[0]
    SQL_MANUFACTURER_COUNT = statistics_sql[1]
    SQL_PRODUCT_COUNT = statistics_sql[2]
    SQL_CATEGORY_COUNT = statistics_sql[3]
    SQL_MANAGER_COUNT = statistics_sql[4]
    SQL_MANAGER_ACTIVE_COUNT = statistics_sql[5]
    SQL_UNMANAGED_COUNT = statistics_sql[6]
    SQL_TRANSACTION_COUNT = statistics_sql[7]
    SQL_SALE_COUNT = statistics_sql[8]
    SQL_HOLIDAY_COUNT = statistics_sql[9]
    SQL_DATABASE_NAME = statistics_sql[10]
    SQL_SYSTEM_USER = statistics_sql[11]
    conn = aux.get_connection()
    if not conn[0]:
        return False, conn[1]
    db = conn[1]
    try:
        cursor = db.cursor()
        cursor.execute(SQL_STORE_COUNT)
        store_count = cursor.fetchone()
        cursor.execute(SQL_MANUFACTURER_COUNT)
        manufacturer_count = cursor.fetchone()
        cursor.execute(SQL_PRODUCT_COUNT)
        product_count = cursor.fetchone()
        cursor.execute(SQL_CATEGORY_COUNT)
        category_count = cursor.fetchone()
        cursor.execute(SQL_MANAGER_COUNT)
        manager_count = cursor.fetchone()
        cursor.execute(SQL_MANAGER_ACTIVE_COUNT)
        manager_active_count = cursor.fetchone()
        cursor.execute(SQL_UNMANAGED_COUNT)
        unmanaged_count = cursor.fetchone()
        cursor.execute(SQL_TRANSACTION_COUNT)
        transaction_count = cursor.fetchone()
        cursor.execute(SQL_SALE_COUNT)
        sale_count = cursor.fetchone()
        cursor.execute(SQL_HOLIDAY_COUNT)
        holiday_count = cursor.fetchone()
        cursor.execute(SQL_DATABASE_NAME)
        db_name = cursor.fetchone()
        cursor.execute(SQL_SYSTEM_USER)
        sys_user_name = cursor.fetchone()
        db.close()
        return True, store_count[0], manufacturer_count[0], product_count[0], category_count[0], manager_count[0], manager_active_count[0], unmanaged_count[0], transaction_count[0], sale_count[0], holiday_count[0], db_name[0], sys_user_name[0]
    except pymysql.Error as pe:
        _, message = pe.args
        return False, message
    except:
        return False, 'SQL file is corrupt. Unable to continue.'


@app.route('/')
@app.route('/index')
def index():
    stats = get_statistics()
    # dbName = aux.get_scalar("SELECT DATABASE()")
    if stats[0]:
        return render_template('index.html', title='Home',
                               table=(('Number of Stores', stats[1]),
                                        ('Number of Manufacturers', stats[2]),
                                        ('Number of Products', stats[3]),
                                        ('Number of Product Categories', stats[4]),
                                        ('Number of Managers', stats[5]),
                                        ('Number of Active Managers', stats[6]),
                                        ('Number of Unmanaged Stores', stats[7]),
                                        ('Number of Transactions', stats[8]),
                                        ('Number of Product Sale Events', stats[9]),
                                        ('Number of Holidays', stats[10])),
                               dbName=stats[11],
                               sysUserName=stats[12],
                               host=mydbconfig.DB_HOST,
                               errorMessage=None)
    return render_template('index.html', title='Home', errorMessage=stats[1])