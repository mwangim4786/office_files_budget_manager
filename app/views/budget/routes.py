#!/usr/bin/python3
"""

"""


from flask import render_template, request, url_for, flash, redirect, abort, session, Blueprint
import uuid
from app import db, bcrypt
from app.views.budget.forms import BudgetForm
from app.models.budget import Budget
from app.models.transactions import Transaction
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
import json

budgetz = Blueprint('budgetz', __name__)


@budgetz.route('/budgets')
@login_required
def budgets():
    budgets = Budget.query.all()
    return render_template('budgets.html', page='budgets', title='Budgets', budgets=budgets)


@budgetz.route('/approvals')
@login_required
def approvals():
    budgets = Budget.query.filter(Budget.user_id != current_user.id).all()
    return render_template('approvals.html', page='approvals', title='Approvals', budgets=budgets)


@budgetz.route('/new_budget/new', methods=['POST', 'GET'])
@login_required
def create_budget():
    budgets = Budget.query.all()
    form = BudgetForm()
    bdgt_id = str(uuid.uuid4())
    available_funds = 100000
    funds_list = []
    for budget in budgets:
        budget_amount = budget.amount
        funds_list.append(budget_amount)
    budget_funds = sum(funds_list)

    
    if form.validate_on_submit():
        if available_funds >= budget_funds + form.amount.data:
            budget = Budget(budget_id=bdgt_id, amount=form.amount.data, bdgt_name=form.name.data, purpose=form.purpose.data, phone=current_user)
            db.session.add(budget)
            db.session.commit()
            flash('Your budget has been created. Await Approval!', 'success')
            return redirect(url_for('budgetz.budgets'))
        else:
            flash('Insufficient funds. Please top up account!', 'warning')
            return redirect(url_for('budgetz.create_budget'))
    return render_template('create_budget.html', page='budgets', title='Create New Budget',
                           form=form, legend='New Budget')
    

@budgetz.route("/budget/<int:budget_id>/update", methods=['POST', 'GET'])
def budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)

    # ---------------------------------------------
    transactions = Transaction.query.filter_by(budget=budget_id).all()
    trans_amnt_list = []
    if transactions:
        for trans in transactions:
            trans_amount = trans.amount
            trans_amnt_list.append(trans_amount)
    utilised_funds = sum(trans_amnt_list)
    available_funds = budget.amount - utilised_funds
    # ---------------------------------------------

    purposeEditVal = json.loads(budget.purpose)
    urls = request.path
    urls = urls.split('/')
    urls = urls[-1]
    if budget.phone != current_user:
        abort(403)
    form = BudgetForm()
    if form.validate_on_submit():
        if budget.status == 1:
            flash('Your budget is Approved. You cannot Update!', 'warning')
            return redirect(url_for('budgetz.budgets'))
        else:
            budget.amount = form.amount.data
            budget.purpose = form.purpose.data
            budget.bdgt_name = form.name.data
            budget.status = 0
            db.session.commit()
            flash('Your budget has been Updated. Await Approval!', 'success')
            return redirect(url_for('budgetz.budgets'))
    elif request.method == 'GET':
        form.amount.data = budget.amount
        form.purpose.data = budget.purpose
        form.name.data = budget.bdgt_name
    return render_template('create_budget.html', page='budgets', title='Update Budget', available_funds=available_funds, budget=budget, edit_vals=purposeEditVal, url=urls, ad_class = 'disabled', form=form, del_id=budget.id, phone=budget.phone, legend='Update Budget')


@budgetz.route("/budget/<int:budget_id>/delete", methods=['POST'])
def delete_budget(budget_id):
    budget = Budget.query.get_or_404(budget_id)
    if budget.phone != current_user:
        abort(403)
    db.session.delete(budget)
    db.session.commit()
    flash('Your budget has been Deleted!', 'success')
    return redirect(url_for('budgetz.budgets'))


@budgetz.route('/budget/<int:budget_id>/view', methods=['GET'])
def view_budget(budget_id):
        
    form = BudgetForm()
    budget = Budget.query.get_or_404(budget_id)
    budget_ppse = json.loads(budget.purpose)
    budget_user = budget.phone.phone

    return render_template('confirm_budget.html', form=form, budget=budget, budget_ppse=budget_ppse, page='approvals', title='Confirm Budget', user=budget_user,
                           delete_bdgt='<a role="button" class="btn btn-outline-danger btn-sm" data-toggle="modal" data-target="#deleteModal">Delete Budget</a>')


@budgetz.route('/approvals/<int:budget_id>/confirm_budget/<string:approve_string>', methods=['POST', 'GET'])
def approve_budget(budget_id, approve_string):
        
    budget = Budget.query.get_or_404(budget_id)
    if approve_string == 'approve':
        budget.status = 1
        budget.approved_by = current_user.name
        db.session.commit()
        flash('Budget has been Approved!', 'success')
        return redirect(url_for('budgetz.approvals'))
    elif approve_string == 'disapprove':
        budget.status = 2
        budget.approved_by = current_user.name
        db.session.commit()
        flash('Budget has been Dispproved!', 'danger')
        return redirect(url_for('budgetz.approvals'))
