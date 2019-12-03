from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import auxFunctions as aux

SQL_PATH = app.root_path + "/sql"
SQL_MANUFACTURER_SUMMARY = aux.getSqlStatementFromFile(SQL_PATH, "06. Display Manufacturer Summary.sql")
SQL_MANUFACTURER_DIS = aux.getSqlStatementFromFile(SQL_PATH, "07a. Display Manufacturer Drill-Down Details.sql")
SQL_MANUFACTURER_DTS = aux.getSqlStatementFromFile(SQL_PATH, "07b. Display Manufacturer Drill-Down Details.sql")
SQL_MANUFACTURER_HEADER = aux.getSqlStatementFromFile(SQL_PATH, "07c. Display Manufacturer Drill-Down Details.sql")


@app.route('/manufacturer_products/', defaults={'manufacturer': ''})
@app.route('/manufacturer_products/<manufacturer>/')
def manufacturer_products(manufacturer):
    if manufacturer == '':
        # initial display
        summaryTable = aux.get_table2(SQL_MANUFACTURER_SUMMARY)
        return render_template('manufacturer_products.html', title="Manufacturers' Products", summary_table=summaryTable)
    # drill-down display
    ret = aux.get_table_rl(SQL_MANUFACTURER_HEADER, [manufacturer])
    if not ret[0]:
        flash(ret[1])
        redirect(manufacturer_products)
    header = ret[1]
    manufacturer_details = aux.get_table1_5(SQL_MANUFACTURER_DTS, manufacturer)
    return render_template('manufacturer_products.html',
                           manufacturer=manufacturer,
                           header=header,
                           manufacturer_details=manufacturer_details,
                           drillTitle='Manufacturer Drill Down')


'''
    if request.method =='GET':
        table = aux.get_table2(SQL_MANUFACTURER_SUMMARY)
        return render_template('manufacturer_products.html', title="Manufacturers' Products", table=table)

    else:
        param = request.get_data(as_text =True)
        #table = get_table2(SQL_MANUFACTURER_SUMMARY)
        #discount = get_table3(SQL_MANUFACTURER_DIS,param)
        #manufacturer_details = get_table3(SQL_MANUFACTURER_DTS,param)
        print(param)
        # https://stackoverflow.com/questions/34214807/python-flask-different-render-template-for-get-and-post-methods-possible
        return redirect(url_for('manufacturer_products_drill', manufacturer_name=param))

        #return render_template('manufacturer_products_drill.html', title="Manufacturers' Products Drill", manufacturer_name=param, manufacturer=manufacturer_details)
'''

@app.route('/manufacturer_products_drill',methods=['GET','POST'])
def manufacturer_products_drill():
    manufacturersName = request.args['manufacturer_name']
    summaryTable = aux.get_table2(SQL_MANUFACTURER_SUMMARY)
    discount = aux.get_table1_5(SQL_MANUFACTURER_DIS, manufacturersName)
    manufacturer_details = aux.get_table1_5(SQL_MANUFACTURER_DTS, manufacturersName)
    return render_template('manufacturer_products_drill2.html', title="Manufacturers' Products Drill",
                           manufacturer_name=manufacturersName, manufacturer_discount=discount,
                           manufacturer_details=manufacturer_details, summary_table=summaryTable)
