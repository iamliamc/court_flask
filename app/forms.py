#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      thoma_000
#
# Created:     21/08/2015
# Copyright:   (c) thoma_000 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SearchForm(Form):
    category = StringField('category')

class ResultsForm(Form):
    category = StringField('category')
    page = IntegerField('page')