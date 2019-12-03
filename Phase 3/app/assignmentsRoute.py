from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
import auxFunctions as aux


def get_assign_sql():
    sql = aux.getSqlSplit('04. Assign Stores.sql')
    if not sql[0]:
        return False, 'Unable to read SQL statements. Cannot continue!!!'
    assign_sql = sql[1]
    SQL_BY_MANAGER = assign_sql[0]
    SQL_BY_STORE = assign_sql[1]
    SQL_INSERT = assign_sql[2]
    SQL_DELETE = assign_sql[3]
    SQL_UNMANAGED_LIST = assign_sql[4]
    SQL_FULL = assign_sql[5]
    SQL_STORES = assign_sql[6]
    SQL_MANAGERS = assign_sql[7]
    return True, (SQL_BY_MANAGER,
                  SQL_BY_STORE,
                  SQL_INSERT,
                  SQL_DELETE,
                  SQL_UNMANAGED_LIST,
                  SQL_FULL,
                  SQL_STORES,
                  SQL_MANAGERS)


@app.route('/assignments', methods=['GET', 'POST'])
def assignments():
    assignmentForm = AssignmentForm(request.form)
    assign_sql = get_assign_sql()
    if not assign_sql[0]:
        flash(assign_sql[1])
        return render_template('assignments.html', title='Assignments', table='', unmanageList='', form=assignmentForm)
    sql = assign_sql[1]
    ret = aux.get_table_rl(sql[5])
    if not ret[0]:
        flash(ret[1])
        return render_template('assignments.html', title='Assignments', table='', unmanageList='', form=assignmentForm)
    table = ret[1]
    unmanaged = aux.get_scalar(sql[4])
    if not unmanaged[0]:
        flash(unmanaged[1])
        return render_template('assignments.html', title='Assignments', table='', unmanageList='')
    unmanagedList = unmanaged[1][0]
    if unmanagedList is None:
        unmanagedList = 'None found'
    ret = aux.get_table_rl(sql[6])
    if not ret[0]:
        flash(ret[1])
        return render_template('assignments.html', title='Assignments', table='', unmanageList='', form=assignmentForm)
    stores = ret[1]
    ret = aux.get_table_rl(sql[7])
    if not ret:
        flash(ret[1])
        return render_template('assignments.html', title='Assignments', table='', unmanageList='', form=assignmentForm)
    managers = ret[1]
    assignmentForm.managerDDL.choices = managers
    assignmentForm.storeDDL.choices = stores

    if request.method == 'POST':
        if assignmentForm.assignManager.data:
            # assign manager to store
            flash("Assigning manager with email %s to store number %s" % (assignmentForm.managerDDL.data, assignmentForm.storeDDL.data))
            ret = aux.writeQuery(sql[2], (assignmentForm.storeDDL.data, assignmentForm.managerDDL.data))
            if not ret[0]:
                flash(ret[1])
                return render_template('assignments.html', title='Assignments', table=table, unmanageList=unmanagedList, form=assignmentForm)
            flash("Manager with email %s successfully assigned to store number %s" % (assignmentForm.managerDDL.data, assignmentForm.storeDDL.data))
            return redirect(url_for('assignments'))

        if assignmentForm.unassignManager.data:
            # unassign manager from store
            flash("Unassigning manager with email %s from store number %s" % (assignmentForm.managerDDL.data, assignmentForm.storeDDL.data))
            ret = aux.writeQuery(sql[3], (assignmentForm.managerDDL.data, assignmentForm.storeDDL.data))
            if not ret[0]:
                flash(ret[1])
                return render_template('assignments.html', title='Assignments', table=table, unmanageList=unmanagedList, orm=assignmentForm)
            flash("Manager with email %s successfully unassigned from store number %s" % (assignmentForm.managerDDL.data, assignmentForm.storeDDL.data))
            return redirect(url_for('assignments'))

    return render_template('assignments.html', title='Assignments', table=table, unmanagedList=unmanagedList, form=assignmentForm)


class AssignmentForm(FlaskForm):
    storeDDL = SelectField('<br>Store Number:')
    managerDDL = SelectField('<br>Manager (email):')
    assignManager = SubmitField('Assign Manager to Store')
    unassignManager = SubmitField('Unassign Manager from Store')
