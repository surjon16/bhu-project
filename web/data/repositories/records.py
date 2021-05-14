from data.models    import Accounts, Roles, Inventory, Appointments, Status, Notifications, Services, Items
from data           import db

from flask_login    import login_user, current_user
from sqlalchemy     import extract, or_, and_, func
from sqlalchemy.sql import label
from datetime       import datetime

import requests, json
import os

itexmo_hdr = {'content-type': 'application/x-www-form-urlencoded'}
itexmo_url = "https://www.itexmo.com/php_api/api.php"
itexmo_api = 'ST-LEONE670607_8GLTB1'
itexmo_pwd = 'm6}}ktrp{{'

class RecordsRepo:

    # ==================================================================================
    # RECORDS
    
    def readRecords():
        return Appointments.query.filter(Appointments.record_details.isnot(None)).order_by(Appointments.record_date.asc()).all()

    def readMonthlyRecords(date):
        data = Appointments.query.filter(Appointments.record_details.isnot(None)).filter(extract('year', Appointments.record_date) == int(date[0:4]), extract('month', Appointments.record_date) == int(date[5:])).all()
        return data

    def readRecord(id):
        return Appointments.query.filter_by(id=id).first()
    
    def searchRecords(id):
        return Appointments.query.filter(Appointments.record_details.isnot(None)).filter_by(account_id=id).order_by(Appointments.record_date.asc()).all()
    
    def upsertRecord(request):

        data = Appointments.query.filter_by(id=request['id']).first()

        data.record_number      = request['record_number']    
        data.record_details     = request['record_details']    
        data.record_date        = request['record_date']    
        data.next_appointments  = request['next_appointments']    

        db.session.commit()

        return True

    def deleteRecord(request):

        data = Appointments.query.filter_by(id=request['id']).first()

        data.record_number      = None
        data.record_details     = None
        data.record_date        = None
        data.next_appointments  = None

        db.session.commit()

        return True
