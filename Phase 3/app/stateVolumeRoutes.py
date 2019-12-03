from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
import auxFunctions as aux

SQL_PATH = app.root_path + "/sql"
MONTH_YEAR_DROPDOWN = aux.getSqlStatementFromFile(SQL_PATH, "12.1 Display State Volume by Category.sql")
STATE_VOLUME_REPORT = aux.getSqlStatementFromFile(SQL_PATH, "12.2 Display State Volume by Category.sql")
STORE_DETAIL_REPORT = aux.getSqlStatementFromFile(SQL_PATH, "12.3 Display State Volume by Category.sql")


@app.route('/state_volume/', defaults={'state': '', 'category': '', 'units': '', 'monthYear': ''}, methods=['GET', 'POST'])
@app.route('/state_volume/<state>/<category>/<units>/<monthYear>/', methods=['GET', 'POST'])
def state_volume(state, category, units, monthYear):
	ret = aux.get_table_rl(MONTH_YEAR_DROPDOWN)
	if not ret[0]:
		flash(ret[1])
		return render_template('state_volume.html', title='Store Revenue', monthsYears='')
	monthsYears = ret[1]
	ddlMonthsYears = [(m_y, m_y) for (m_y,) in monthsYears]
	stateVolumeForm = StateVolumeForm()
	stateVolumeForm.monthYearDDL.choices = ddlMonthsYears

	# monthYearDropDownTable = list(aux.get_table2(MONTH_YEAR_DROPDOWN))
	# monthYearDropDownResult = list(monthYearDropDownTable)

	if request.method == 'POST':
		# the Generate button was clicked

		# app.logger.warning('[APP_LOG] Selected Month Year:  %s', request.form.get("selected_month_year"))
		# param = request.form.get("selected_month_year")
		# param = param.split("-")

		monthYear = stateVolumeForm.monthYearDDL.data
		monthYearList = monthYear.split('-')
		month = monthYearList[0]
		year = monthYearList[1]
		parameterList = [month, year, month, year]
		ret = aux.get_table_rl(STATE_VOLUME_REPORT, parameterList)
		if not ret[0]:
			flash(ret[1])
			return render_template('state_volume.html', title='State Volume', state_volume='')
		stateVolReport = ret[1]
		return render_template('state_volume.html',
								title='State Volume Drill',
								form=stateVolumeForm,
								state_vol=stateVolReport,
								monthYear=monthYear)

		# stateVolReport = aux.get_table4(STATE_VOLUME_REPORT, param)
		# stateVolReport = tuple(zip(stateVolReport.Category, stateVolReport.State, stateVolReport.Units))
		# # converting into a tuple of tuples so jinja2 can iterate in the template
		#
		# return render_template('state_vol_drill.html',
		# 					   title='State Volume Drill',
		# 					   form=stateVolumeForm,
		# 					   state_vol=stateVolReport,
		# 					   month_years=monthYear)

	else:
		# either this is the initial display of the page, or we are drilling
		if state == '':
			# this is the initial display of the page
			return render_template('state_volume.html', title='State Volume', form=stateVolumeForm)
		else:
			# we are drilling
			table = aux.get_table1_5(STORE_DETAIL_REPORT, state)
			return render_template('state_volume.html', title='State Volume', form=stateVolumeForm,
									table=table, state=state, category=category, units=units, monthYear=monthYear)


# @app.route('/store_details')
# def store_details():
# 	stateName = request.args['state']
# 	categoryName = request.args['category']
# 	units = request.args['units']
# 	table = aux.get_table1_5(STORE_DETAIL_REPORT, stateName)
# 	return render_template('store_details.html', title='Store Details', table=table, category=categoryName,
# 						   state = stateName, units=units)
#
#
# @app.route('/delete_me_store_revenue2', methods=['GET', 'POST'])
# def store_revenue2():
# 	stateSQLResult = aux.get_df(SELECT_MANAGERS_SQL)
# 	state_sql = '''SELECT DISTINCT state FROM City ORDER BY state;'''
# 	states = list(get_table2(state_sql))
#
# 	if request.method =='POST':
# 		param = request.form.get("selected_state")
# 		stores = get_table2(SQL_STORE_REVENUE,param)
# 		# todo make code use submit bootstrap styling, like manager/
# 		return render_template('store_revenue.html', title='Store Revenue', states=states, stores=stores, state_nam=param)
#
# 	return render_template('store_revenue.html', title='Store Revenue', states=states)


class StateVolumeForm(FlaskForm):
    monthYearDDL = SelectField('<br>Select month-year from which to list highest volume stores in each category:')
    generate = SubmitField('Generate')
