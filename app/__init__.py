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

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
from app import views, models