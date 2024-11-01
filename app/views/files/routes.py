#!/usr/bin/python3

from flask import render_template, request, url_for, flash, redirect, abort, session, Blueprint
from app import db, bcrypt
from app.views.files.forms import FileForm
from app.models.files import Files
from app.models.transactions import Transaction
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required

filez = Blueprint('filez', __name__)


@filez.route('/new_file/new', methods=['POST', 'GET'])
@login_required
def create_file():
    files = Files.query.all()

    form = FileForm()
    if form.validate_on_submit():
        file = Files(file_no=form.file_no.data, file_name=form.file_name.data, subject=form.subject.data, file_fee=form.file_fee.data)
        db.session.add(file)
        db.session.commit()
        flash('File created successfuly!', 'success')
        return redirect(url_for('filez.files'))
    elif request.method == 'GET':
        if len(files) == 0:
            form.file_no.data = '100/1/C'
        elif len(files) > 0:
            file_list = []
            def_val = 0
            for file in files:
                val = file.file_no
                val = val.split('/')
                no_val = val[0]
                file_list.append(no_val)
            initial_val = int(max(file_list))+1
            def_val = str(initial_val)+'/1/C'
            form.file_no.data = def_val
    return render_template('create_file.html', page='files', title='Create New file',
                           form=form, legend='New File')


@filez.route('/files')
@login_required
def files():
    
    files = Files.query.all()
    if len(files) == 0:
        count = 0
    else:
        count = len(files)

    return render_template('files.html', page='files', files=files, count=count)


@filez.route('/files/<int:file_id>/view', methods=['GET'])
def view_file(file_id):
        
    file_info = Files.query.get_or_404(file_id)
    fileName = file_info.file_name
    fileNo = file_info.file_no
    file_totals = []

    transactions_per_file = Transaction.query.filter_by(file=fileNo).all()
    for trns_cost in transactions_per_file:
        cost = trns_cost.amount
        file_totals.append(cost)
    
    file_costs = sum(file_totals)

    return render_template('view_file.html', file=file_info, page='files', title=fileNo+" - "+fileName, transactions=transactions_per_file, file_costs=file_costs)

