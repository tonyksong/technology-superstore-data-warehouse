from flask import render_template, flash, redirect, url_for
from app import app
import auxFunctions as aux


SQL_PATH = app.root_path + "/sql"
SQL_STORE_REVENUE_BY_STATE = aux.getSqlStatementFromFile(SQL_PATH, "10. Display Store Revenue by Year and State.sql")
SQL_GROUNDHOG = aux.getSqlStatementFromFile(SQL_PATH, "14. Display Groundhog Day.sql")
SQL_CATEGORY_SUMMARY = aux.getSqlStatementFromFile(SQL_PATH, "08. Category Summary.sql")

# todo: rename holidayRoutes.py to holidaysRoute.py for consistency
# todo: rename managerRoutes.py to managersRoute.py for consistency
# todo: rename populationRoute.py to populationsRoute.py for consistency

# @app.route('/') and @app.route('/index') now located in app/homeRoute.py
# @app.route('/holidays') now located in app/holidayRoutes.py
# @app.route('/managers', methods=['GET', 'POST']) now located in app/managerRoutes.py
# @app.route('/assignments') now located in app/assignmentsRoute.py
# @app.route('/populations') now located in app/populationRoute.py

# @app.route('/manufacturer_products',methods=['GET','POST']) now located in app/manufacturerRoutes.py
# along with @app.route('/manufacturer_products_drill',methods=['GET','POST'])

# @app.route('/state_volume') now located in app/stateVolumeRoutes.py
# along with @app.route('/store_details')

# @app.route('/store_revenue', methods=['GET', 'POST']) now located in app/populationRoute.py

# Routes below are limited to pages that only display simple tables


@app.route('/categories')
def categories():
    table = aux.get_table2_5(SQL_CATEGORY_SUMMARY)
    return render_template('categories.html', title='Categories', table=table)


@app.route('/gps')
def gps():
    ret = aux.getSql("09.2. Display Actual vs Predicted GPS.sql")
    if ret[0]:
        sql = ret[1]
        ret = aux.get_table_rl(sql)
        if ret[0]:
            sqlOutput = ret[1]
            return render_template('gps.html', title='GPS', table=sqlOutput)
        flash(ret[1])
        return render_template('gps.html', title='GPS', table='')
    flash(ret[1])
    return render_template('gps.html', title='GPS', table='')


@app.route('/gh_day')
def gh_day():
    table = aux.get_table2_5(SQL_GROUNDHOG)
    return render_template('gh_day.html', title='Groundhog Day', table=table)


@app.route('/population_revenue')
def population_revenue():
    # table1 = aux.get_table2_5(SQL_TOTAL_REV_BY_POP)
    # table2 = aux.get_table2_5(SQL_AVG_REV_BY_POP)
    ret = aux.getSql('13.2. Display Annual Average Revenue by City Population.sql')
    if not ret[0]:
        flash(ret[1])
        return render_template('population_revenue.html', title='Population Revenue', tables=[], titles=[])
    sql = ret[1]
    ret = aux.get_two_tables(sql)
    if not ret[0]:
        flash(ret[1])
        return render_template('population_revenue.html', title='Population Revenue', tables=[], titles=[])
    return render_template('population_revenue.html', title='Population Revenue', tables=[ret[1], ret[2]],
                           titles=['na',
                                   'Total Revenue Over All Stores by Year and Population Category',
                                   'Average Revenue Over All Stores by Year and Population Category'])
