#!/usr/bin/python3
"""

"""

from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class BudgetForm(FlaskForm):
    amount = IntegerField('Amount',
                           validators=[DataRequired()])
    
    name = StringField('Name', validators=[DataRequired()])
    
    purpose = StringField('Purpose', validators=[DataRequired()])

    submit = SubmitField('Submit')