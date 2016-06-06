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

from app import db

from collections import OrderedDict

class DictSerializable(object):
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

class Defendant(db.Model):
    defendant_id = db.Column(db.Integer, primary_key=True)
    Name_Full = db.Column(db.Text, index=True)
    Language = db.Column(db.Text, index=True)
    Mailing_Address = db.Column(db.Text, index=True)
    Race = db.Column(db.Text, index=True)
    Sex = db.Column(db.Text, index=True)
    Height = db.Column(db.Text, index=True)
    DOB = db.Column(db.Text, index=True)
    Weight = db.Column(db.Text, index=True)
    Hair = db.Column(db.Text, index=True)
    Eyes = db.Column(db.Text, index=True)
    Case = db.relationship('Case_Info', backref='DefendantPerson', lazy='dynamic')


class Case_Info(db.Model):
    __tablename__ = 'case_info'
    defendant_id = db.Column(db.Integer, db.ForeignKey('defendant.defendant_id'), primary_key=True)
    Case_Number = db.Column(db.Text, index=True)
    Attorney = db.Column(db.Text, index=True)
    Firm = db.Column(db.Text, index=True)
    Attorney_Phone = db.Column(db.Text, index=True)
    Judge = db.Column(db.Text, index=True)


class Charge(db.Model):
    charges_id = db.Column(db.Integer, primary_key=True)
    Case_Number = db.Column(db.Text, db.ForeignKey('case_info.Case_Number'), index=True)
    Offense_Date = db.Column(db.Text, index=True)
    Date_Closed = db.Column(db.Text, index=True)
    Offense = db.Column(db.Text, index=True)
    Disposition = db.Column(db.Text, index=True)
    Disposition_Date = db.Column(db.Text, index=True)
