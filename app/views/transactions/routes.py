#!/usr/bin/python3

from flask import render_template, request, url_for, flash, redirect, abort, session, Blueprint
# from app import db, bcrypt
from app.models.transactions import Transaction
from flask_login import login_user, current_user, logout_user, login_required

transactionz = Blueprint('transactionz', __name__)


@transactionz.route('/transactions')
@login_required
def transactions():

    transactions = []
    bdgt_names = []

    if current_user.role == 'Admin':
        transactions = Transaction.query.all()
    else:
        transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    for transaction in transactions:
        bdgt_names.append(transaction.budget)

    return render_template('transactions.html', page='transactions', transactions=transactions, names=bdgt_names)

