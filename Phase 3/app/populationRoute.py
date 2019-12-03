from flask import render_template, flash, redirect, url_for
from app import app
from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import auxFunctions as aux


def get_population_sql():
    sql = aux.getSqlSplit('05. Update City Population.sql')
    if not sql[0]:
        return False, 'Unable to read SQL statements. Cannot continue!!!'
    population_sql = sql[1]
    SQL_CITY_POPULATIONS = population_sql[0]
    SQL_CITIES = population_sql[1]
    SQL_UPDATE = population_sql[2]
    return True, (SQL_CITY_POPULATIONS,
                  SQL_CITIES,
                  SQL_UPDATE)


@app.route('/populations', methods=['GET', 'POST'])
def populations():
    populationForm = PopulationForm()
    population_sql = get_population_sql()
    if not population_sql[0]:
        flash(population_sql[1])
        return render_template('populations.html', title='Populations', table='', unmanageList='', form=assignmentForm)
    sql = population_sql[1]
    ret = aux.get_table_rl(sql[0])
    if not ret[0]:
        flash(ret[1])
        return render_template('populations.html', title='Populations', table='', unmanageList='', form=assignmentForm)
    table = ret[1]
    ret = aux.get_table_rl(sql[1])
    if not ret[0]:
        flash(ret[1])
        return render_template('populations.html', title='Populations', table='', unmanageList='', form=assignmentForm)
    cities = ret[1]
    populationForm.cityDDL.choices = cities
    if populationForm.validate_on_submit():
        combined = populationForm.cityDDL.data.split('|')
        city = combined[0]
        state = combined[1]
        flash("Updating population of %s, %s" % (city, state))
        resultWrite = aux.writeQuery(sql[2], paramList=[populationForm.population.data, city, state])
        if resultWrite[0]:
            flash("Successfully updated population of %s, %s" % (city, state))
            return redirect(url_for('populations'))
        else:
            flash(resultWrite[1])
            return render_template('populations.html', form=populationForm, title='City Populations', table=table)
    else:
        return render_template('populations.html', form=populationForm, title='City Populations', table=table)


class PopulationForm(FlaskForm):
    cityDDL = SelectField('<br>City: ')
    population = IntegerField('New Population: ', validators=[DataRequired('You must enter a new population as a positive integer.'), NumberRange(min=1, max=4294967295, message='Please enter an integer between 1 and 4294967295, inclusive')])
    submit = SubmitField('Change')
