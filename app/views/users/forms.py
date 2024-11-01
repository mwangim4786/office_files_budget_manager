#!/usr/bin/python3
"""

"""

from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models.users import Users
from app.models.files import Files
from app.models.budget import Budget

class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=200)])
    # username = StringField('Username',
    #                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=200)])
    
    role = StringField('Role',
                           validators=[DataRequired(), Length(min=2, max=200)])
    
    date = StringField('Date',
                           validators=[DataRequired(), Length(min=2, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address is taken. Please chose another.')
        
    def validate_phone(self, phone):
        user = Users.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Phone number is taken. Please chose another.')




class UpdateUserForm(FlaskForm):
    id = IntegerField('Id')
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField('Email',
                           validators=[DataRequired(), Email()])
    
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=200)])
    
    role = StringField('Role',
                           validators=[DataRequired(), Length(min=2, max=200)])
    
    date = StringField('Date',
                           validators=[DataRequired(), Length(min=2, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user == current_user:
                raise ValidationError('Email address is taken. Please chose another.')
        
    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = Users.query.filter_by(phone=phone.data).first()
            if user == current_user:
                raise ValidationError('Phone number is taken. Please chose another.')

class LoginForm(FlaskForm):
    phone = StringField('Phone',
                           validators=[DataRequired(), Length(min=2, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')