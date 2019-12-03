from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
import auxFunctions as aux


# SELECT_MANAGERS_SQL = "SELECT managerName AS `Manager`, emailAddress AS `Email` FROM Manager ORDER BY managerName;"
# INSERT_NEW_MANAGER_SQL = "INSERT INTO Manager(emailAddress, managerName) VALUES (%s,%s);"
# UPDATE_MANAGER_SQL = "UPDATE Manager SET managerName = %s WHERE emailAddress = %s;"
# DEACTIVATE_MANAGER_SQL = "DELETE FROM Manages WHERE emailAddress = %s;"
# FIND_MANAGER_ASSIGNMENTS_SQL = "SELECT storeNumber, emailAddress FROM Manages WHERE emailAddress= %s;"
# REMOVE_MANAGER_ASSIGNMENTS_SQL = "DELETE FROM Manager WHERE emailAddress = %s;"
# COUNT_MANAGER_ASSIGNMENTS_SQL = "SELECT COUNT(emailAddress) FROM Manages WHERE emailAddress= %s;"
# DELETE_MANAGER_SQL = "DELETE FROM Manager WHERE emailAddress = %s;"


@app.route('/managers', methods=['GET', 'POST'])
def managers():
    managerForm = ManagerForm(request.form)

    ret = aux.getSqlSplit('03. Edit Manager Profile.sql')
    if not ret[0]:
        flash(ret[1])
        return render_template('managers.html', form=managerForm, title='Managers', table='')
    manager_sql = ret[1]
    SELECT_MANAGERS_SQL = manager_sql[0]
    INSERT_NEW_MANAGER_SQL = manager_sql[1]
    UPDATE_MANAGER_SQL = manager_sql[2]
    DEACTIVATE_MANAGER_SQL = manager_sql[3]
    FIND_MANAGER_ASSIGNMENTS_SQL = manager_sql[4]
    REMOVE_MANAGER_ASSIGNMENTS_SQL = manager_sql[5]
    COUNT_MANAGER_ASSIGNMENTS_SQL = manager_sql[6]
    DELETE_MANAGER_SQL = manager_sql[7]

    resultGet = aux.get_table_rl(SELECT_MANAGERS_SQL)
    if resultGet[0]:
        sqlOutput = resultGet[1]
        managerForm.managersDDL.choices = [(email, "%s (%s)" % (name, email)) for (name, email) in sqlOutput]
        if request.method == 'POST':
            if managerForm.deactivateManager.data:
                # deactivate manager
                flash("Deactivating manager %s" % dict(managerForm.managersDDL.choices).get(managerForm.managersDDL.data))
                resultWrite = aux.writeQuery(DEACTIVATE_MANAGER_SQL, paramList=[managerForm.managersDDL.data])
                if resultWrite[0]:
                    flash("Successfully deactivated manager %s" % dict(managerForm.managersDDL.choices).get(
                        managerForm.managersDDL.data))
                    return redirect(url_for('managers'))
                else:
                    flash(resultWrite[1])
                    return redirect(url_for('managers'))
            elif managerForm.deleteManager.data:
                # delete manager
                flash("Deleting manager %s" % dict(managerForm.managersDDL.choices).get(managerForm.managersDDL.data))
                resultGet = aux.get_scalar(COUNT_MANAGER_ASSIGNMENTS_SQL, paramList=managerForm.managersDDL.data)
                if resultGet[0]:
                    if resultGet[1][0] == 0:
                        resultWrite = aux.writeQuery(DELETE_MANAGER_SQL, paramList=managerForm.managersDDL.data)
                        if resultWrite[0]:
                            flash("Successfully deleted manager %s" % dict(managerForm.managersDDL.choices).get(
                                managerForm.managersDDL.data))
                            return redirect(url_for('managers'))
                        else:
                            flash(resultWrite[1])
                            return redirect(url_for('managers'))
                    else:
                        flash("Manager %s, must be deactivated before being deleted." % dict(managerForm.managersDDL.choices).get(managerForm.managersDDL.data))
                        return redirect(url_for('managers'))
                else:
                    flash(resultGet[1])
                    return redirect(url_for('managers'))
            elif managerForm.addChange.data and \
                    managerForm.managerEmail.validate(managerForm, extra_validators=[DataRequired("Please enter manager's email address"), Email("Please enter a valid email address")]) and \
                    managerForm.managerName.validate(managerForm, extra_validators=[DataRequired("Please enter manager's name")]):
                    emails = [email for (name, email) in sqlOutput]
                    if (managerForm.managerEmail.data in emails):
                        # existing manager email
                        flash("Updating existing manager: %s (%s)" % (managerForm.managerName.data, managerForm.managerEmail.data))
                        resultWrite = aux.writeQuery(UPDATE_MANAGER_SQL, paramList=[managerForm.managerName.data, managerForm.managerEmail.data])
                        if resultWrite[0]:
                            flash("Updated existing manager: %s (%s)" % (managerForm.managerName.data, managerForm.managerEmail.data))
                            return redirect(url_for('managers'))
                        else:
                            flash(resultWrite[1])
                            return redirect(url_for('managers'))
                    else:
                        # new manager
                        flash("Inserting new manager: %s (%s)" % (managerForm.managerName.data, managerForm.managerEmail.data))
                        resultWrite = aux.writeQuery(INSERT_NEW_MANAGER_SQL, paramList=[managerForm.managerEmail.data, managerForm.managerName.data])
                        if resultWrite[0]:
                            flash("Successfully inserted new manager: %s (%s)" % (managerForm.managerName.data, managerForm.managerEmail.data))
                            return redirect(url_for('managers'))
                        else:
                            flash(resultWrite[1])
                            return redirect(url_for('managers'))
            else:
                return render_template('managers.html', form=managerForm, title='Managers', table=sqlOutput)
        else:
            # todo: FLASH: if an existing one is added , flash a warning message within form.validate_on_submit as illustrated here: https://learning.oreilly.com/library/view/flask-web-development/9781491991725/ch04.html#ch_forms
            # todo  check manager email syntax to match email address if not, flash
            # todo: add logic for deactivate manager
            # todo: add logic for delete manager
            return render_template('managers.html', form=managerForm, title='Managers', table=sqlOutput)
    else:
        flash(resultGet[1])
        # return render_template('managers.html', form=managerForm, title='Managers', table='')
        return redirect(url_for('managers'))


class ManagerForm(FlaskForm):
    managerName = StringField('To Add or Change Manager:<br>Manager Name: ')
    managerEmail = StringField('Manager Email: ', validators=[Email()])
    addChange = SubmitField('Add or Change')
    managersDDL = SelectField('<br>Select Manager to Deactivate or Delete:')
    deactivateManager = SubmitField('Deactivate Manager')
    deleteManager = SubmitField('Delete Manager')
