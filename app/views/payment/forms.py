#!/usr/bin/python3
"""

"""

from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class PayForm(FlaskForm):
    amount = IntegerField('Amount',
                           validators=[DataRequired()])
    
    narration = StringField('Description', validators=[DataRequired(), Length(min=1, max=200)])
    
    paybill = StringField('Paybill', validators=[DataRequired()])

    # file_no = SelectField('Select File', choices=choice_func_file(), validators=[DataRequired()])
    file_no = SelectField('Select File', choices=[], validators=[DataRequired()])

    # budget_no = SelectField('Select Budget', choices=choice_func_budget(), validators=[DataRequired()])
    budget_no = SelectField('Select Budget', choices=[], validators=[DataRequired()])

    submit = SubmitField('Submit')

    def validate_budget_no(self, budget_no):
        if budget_no.data == "wrong-Budgetz":
            raise ValidationError('Please choose a budget from list.')
    
    def validate_file_no(self, file_no):
        if file_no.data == "wrong-Filez":
            raise ValidationError('Please choose a File from list.')