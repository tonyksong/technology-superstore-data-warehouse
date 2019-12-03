from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
import auxFunctions as aux

SQL_PATH = app.root_path + "/sql"
SQL_STORE_REVENUE_BY_STATE = aux.getSqlStatementFromFile(SQL_PATH, "10. Display Store Revenue by Year and State.sql")
SQL_STATE = aux.getSqlStatementFromFile(SQL_PATH, "10.1. Display Store Revenue by Year and State.sql")


@app.route('/store_revenue', methods=['GET', 'POST'])
def store_revenue():
    # state_sql = '''SELECT DISTINCT state FROM City ORDER BY state;'''
    # states = list(aux.get_table2(SQL_STATE))
    ret = aux.get_table_rl(SQL_STATE)
    if not ret[0]:
        flash(ret[1])
        return render_template('store_revenue.html', title='Store Revenue', states='')
    states = ret[1]
    ddlStates = [(st, st) for (st,) in states]
    storeRevenueForm = StoreRevenueForm()
    storeRevenueForm.storeDDL.choices = ddlStates

    if request.method == 'POST':
        # param = request.form.get("selected_state")
        # stores = aux.get_table2_5(SQL_STORE_REVENUE_BY_STATE,param)
        stores = aux.get_table2_5(SQL_STORE_REVENUE_BY_STATE, storeRevenueForm.storeDDL.data)
        return render_template('store_revenue.html', title='Store Revenue', states=ddlStates,
                               table=stores, state=storeRevenueForm.storeDDL.data,
                               form=storeRevenueForm)

    return render_template('store_revenue.html', title='Store Revenue', states=ddlStates, state=None, table=None, form=storeRevenueForm)


class StoreRevenueForm(FlaskForm):
    storeDDL = SelectField('<br>Select state from which to list stores and their revenue:')
    generate = SubmitField('Generate')
