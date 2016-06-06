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

#!flask/bin/python
from app import app
app.run(debug=True, host='localhost', port=5000)
