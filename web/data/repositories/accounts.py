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


class AccountsRepo:
    # ==================================================================================
    # ACCOUNTS

    def loginAccount(request):
        data = Accounts.query.filter_by(email=request['email']).first()
        if data is not None and data.verify_password(request['password']):
            login_user(data)
            return data
        else:
            return False

    def readAccounts():
        return Accounts.query.all()

    def readRegisteredAccounts():
        return Accounts.query.filter(Accounts.role_id.in_([1,2,3])).all()
    
    def readResidentAccounts():
        return Accounts.query.filter(or_(Accounts.role_id.is_(None), Accounts.role_id == 3)).all()
    
    def readAccount(id):
        return Accounts.query.filter_by(id=id).first()

    def registerAccount(request):
        data = Accounts(
            first_name  = request['first_name'],
            last_name   = request['last_name'],
            phone       = request['phone'],
            email       = request['email'],
            password    = request['password']
        )
        db.session.add(data)
        db.session.commit()

        return True

    def upsertAccount(request):

        data = Accounts.query.filter_by(id=request['id']).first()

        birth_date = request['birth_date']
        try:
            birth_date = datetime.strptime(birth_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            birth_date = None

        if data == None:

            if request['password']:
                data = Accounts(
                    first_name  = request['first_name'],
                    middle_name = request['middle_name'],
                    last_name   = request['last_name'],
                    gender      = request['gender'],
                    civil       = request['civil'],
                    phone       = request['phone'],
                    birth_date  = birth_date,
                    address     = request['address'],
                    email       = request['email'],
                    password    = request['password'],
                    occupation  = request['occupation'],
                    role_id     = int(request['role_id'])
                )
            else:
                data = Accounts(
                    first_name  = request['first_name'],
                    middle_name = request['middle_name'],
                    last_name   = request['last_name'],
                    gender      = request['gender'],
                    civil       = request['civil'],
                    phone       = request['phone'],
                    birth_date  = birth_date,
                    address     = request['address'],
                    email       = request['email'],
                    occupation  = request['occupation'],
                    role_id     = int(request['role_id'])
                )

            try: 
                db.session.add(data) 
                db.session.commit() 
                return True

            except AssertionError as exception_message: 
                return False
                
        else:

            data.first_name  = request['first_name']
            data.middle_name = request['middle_name']
            data.last_name   = request['last_name']
            data.gender      = request['gender']
            data.civil       = request['civil']
            data.phone       = request['phone']
            data.birth_date  = birth_date
            data.address     = request['address']
            data.email       = request['email']
            data.occupation  = request['occupation']
            data.role_id     = int(request['role_id'])

            if request['password']:
                data.password = request['password']

            db.session.commit()

        return True

    def deleteAccount(request):

        data = Accounts.query.filter_by(id=request['id']).first()
        
        if data == None:
            return False
        else:

            # delete all notifications
            for notification in data.account_notifications:
                db.session.delete(notification)

            for appointment in data.account_appointments:
                db.session.delete(appointments)

            # finally, delete account
            db.session.delete(data)
            db.session.commit()

            return True
