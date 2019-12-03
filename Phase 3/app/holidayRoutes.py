from flask import render_template, flash, redirect, url_for
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
import auxFunctions as aux


@app.route('/holidays', methods=['GET', 'POST'])
def holidays():
    holidayForm = HolidayForm()
    ret = aux.getSqlSplit('02 Edit Holiday Data.sql')
    if not ret[0]:
        flash(ret[1])
        return render_template('holidays.html', form=holidayForm, title='Holidays', table='')
    holiday_sql = ret[1]
    SELECT_HOLIDAYS_SQL = holiday_sql[0]
    INSERT_NEW_HOLIDAY_SQL = holiday_sql[1]
    UPDATE_HOLIDAY_SQL = holiday_sql[2]

    resultGet = aux.get_table_rl(SELECT_HOLIDAYS_SQL)
    if resultGet[0]:
        sqlOutput = resultGet[1]
        if holidayForm.validate_on_submit():
            dateList = [date for (holiday, date) in sqlOutput]
            if holidayForm.holidayDate.data in dateList:
                # existing holiday
                flash("Updating existing holiday date %s" % holidayForm.holidayDate.data)
                resultWrite = aux.writeQuery(UPDATE_HOLIDAY_SQL, paramList=[holidayForm.holidayName.data, holidayForm.holidayDate.data])
                if resultWrite[0]:
                    return redirect(url_for('holidays'))
                else:
                    flash(resultWrite[1])
                    return redirect(url_for('holidays'))
            else:
                # new holiday
                flash("Inserting new holiday (%s on %s)" % (holidayForm.holidayName.data, holidayForm.holidayDate.data))
                resultWrite = aux.writeQuery(INSERT_NEW_HOLIDAY_SQL, paramList=[holidayForm.holidayDate.data, holidayForm.holidayName.data])
                if resultWrite[0]:
                    return redirect(url_for('holidays'))
                else:
                    flash(resultWrite[1])
                    return redirect(url_for('holidays'))
        else:
                return render_template('holidays.html', form=holidayForm, title='Holidays', table=sqlOutput)
    else:
        flash(resultGet[1])
        return render_template('holidays.html', form=holidayForm, title='Holidays', table='')


class HolidayForm(FlaskForm):
    holidayName = StringField('New Holiday Name: ', validators=[DataRequired('You must enter a holiday name.')])
    holidayDate = DateField('Holiday Date: ', validators=[DataRequired('You must enter a holiday name.')], format='%Y-%m-%d')
    submit = SubmitField('Enter')
