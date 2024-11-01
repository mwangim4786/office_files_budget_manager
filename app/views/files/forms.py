#!/usr/bin/python3
"""

"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class FileForm(FlaskForm):

    file_no = StringField('File Number', validators=[DataRequired()])
    file_name = StringField('File Name', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    file_fee = IntegerField('File Fees', validators=[DataRequired()])

    submit = SubmitField('Submit')