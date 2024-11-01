#!/usr/bin/python3

from flask import render_template, request, url_for, flash, redirect, abort, session, Blueprint
from app import app, db, bcrypt
from app.views.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from app.models.users import Users
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required

users = Blueprint('users', __name__)




@users.route("/users")
def allUsers(): # ************************* users *************************
    users = Users.query.all()
    return render_template('users.html', page='users', users=users)


# ************************************* Home *************************************
@users.route('/home')
@login_required
def home():
    return render_template('home.html', page='home',)

# ************************************* Home *************************************

@users.route('/account/<user_id>')
@login_required
def account(user_id):
    user = Users.query.get_or_404(user_id)
    # if user.phone != current_user:
    #     abort(403)
    return render_template('account.html', page='account', title='Account', user=user)



@users.route('/register', methods=['POST', 'GET'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        date_val = form.date.data
        date_value = datetime.strptime(date_val, "%Y-%m-%d")
        user = Users(name=form.name.data, email=form.email.data, phone=form.phone.data, role=form.role.data, password=hashed_pw, date=date_value)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('allUsers'))
    return render_template('register.html', page='register', title='Register', form=form)


@users.route("/user/<int:user_id>/update", methods=['POST', 'GET'])
def user(user_id):
    user = Users.query.get_or_404(user_id)
    
    form = UpdateUserForm()
    if form.validate_on_submit():

        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        date_val = form.date.data
        date_value = datetime.strptime(date_val, "%Y-%m-%d")

        user.name = form.name.data
        user.email = form.email.data
        user.phone = form.phone.data
        user.role = form.role.data
        if user == current_user:
            user.password = hashed_pw

        user.date = date_value

        db.session.commit()
        flash('User has been Updated!', 'success')
        return redirect(url_for('account', user_id=user.id))
    elif request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.role.data = user.role
        form.id.data = user.id
        form.date.data = user.date.strftime('%Y-%m-%d')
    return render_template('register.html', page='users', title='Update user', form=form, del_id=user.id, user=user, legend='Update user')


@users.route("/user/<int:user_id>/delete", methods=['POST'])
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    if current_user.role != 'Admin':
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('User has been Deleted!', 'success')
    return redirect(url_for('allUsers'))


@users.route('/', methods=['POST', 'GET'])
@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(phone=form.phone.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('users.home'))
            # return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccesseful. Check your details!', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))
