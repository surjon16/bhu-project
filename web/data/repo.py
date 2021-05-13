from data.models    import Accounts, Roles, Inventory, Appointments, Status, Notifications, Services
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

class Repository:

    def __init__(self):
        pass

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

    # ==================================================================================
    # APPOINTMENTS
    
    def readAppointments():
        return Appointments.query.order_by(Appointments.status_id.desc(), Appointments.appointment_date.asc()).all()
    
    def readDailyAppointments(date):
        data = Appointments.query.filter(extract('month', Appointments.appointment_date) == int(date[0:2]), extract('day', Appointments.appointment_date) == int(date[3:5]), extract('year', Appointments.appointment_date) == int(date[6:])).order_by(Appointments.status_id.desc(), Appointments.appointment_date.asc()).all()
        return data

    def readAppointment(id):
        return Appointments.query.filter_by(id=id).first()

    def updateAppointmentStatus(request):

        data = Appointments.query.filter_by(id=request['id']).first()
        data.status_id = request['status_id']

        db.session.commit()

        return True

    def upsertAppointment(request):

        data = Appointments.query.filter_by(id=request['id']).first()

        if data == None:
            data = Appointments(
                details             = request['details'],
                appointment_date    = request['appointment_date'],
                assigned            = request['assigned'],
                account_id          = request['account_id'],
                service_id          = request['service_id'],
                status_id           = request['status_id']
            )
            db.session.add(data)

        else:

            data.details             = request['details']
            data.appointment_date    = request['appointment_date']
            data.assigned            = request['assigned']
            data.account_id          = request['account_id']
            data.service_id          = request['service_id']
            data.status_id           = request['status_id']
                
        db.session.commit()

        # =============================================================================================================
        # Create a notification after creating an appointment

        content = 'Hi, ' + str(data.account.first_name) + '. This is from the Barangay Gusa Health Center. We would like to inform you that your requested appointment for ' + str(data.service.service) + ' on ' + str(data.appointment_date.strftime('%h %d %Y %I:%M %p')) + ' is now ' + str(data.status.status) + '. Thank you!'

        notifs = Notifications(content=content, notif_type='app', account_id=data.account.id)
        db.session.add(notifs)
        db.session.commit()

        try:
            
            # Send an sms to the patient.
            sms = {
                '1'         : data.account.phone,
                '2'         : content,
                '3'         : 'ST-LEONE670607_8GLTB',
                'passwd'    : 'm6}}ktrp{{'
            }
            response = requests.post(url=itexmo_url, data=sms)
            print(response.text)

        except:
            
            return True

        # =============================================================================================================
        
        return True

    def deleteAppointment(request):

        data = Appointments.query.filter_by(id=request['id']).first()
        
        if data == None:
            return False
        else:
            db.session.delete(data)
            db.session.commit()
            return True

    # ==================================================================================
    # INVENTORY

    def readInventories():
        return Inventory.query.all()

    def readAvailableItems():
        return Inventory.query.filter_by(status_id=5).group_by(Inventory.item).all()

    def readUsedItems():
        return Inventory.query.filter_by(status_id=6).group_by(Inventory.item).all()

    def readExpiredItems():
        return Inventory.query.filter_by(status_id=7).group_by(Inventory.item).all()

    def readInventoriesGroupByItemAndStatus():
        return db.session.query(Inventory.item, Inventory.status_id, label('status', func.sum(Inventory.quantity))).group_by(Inventory.item, Inventory.status_id).all()

    def readInventoriesGroupByItem():
        return db.session.query(Inventory.item, label('total_stocks', func.sum(Inventory.quantity))).group_by(Inventory.item).all()

    def readInventory(id):
        return Inventory.query.filter_by(id=id).first()

    # def bulkUpsertInventory(request):

    def upsertInventory(request):

        data = Inventory.query.filter_by(id=request['id']).first()

        expiry_date = request['expiry_date']
        try:
            expiry_date = datetime.strptime(expiry_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            expiry_date = None

        receive_date = request['receive_date']
        try:
            receive_date = datetime.strptime(receive_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            receive_date = None

        if data == None:
            data = Inventory(
                item            = request['item'],
                # expiry_date     = expiry_date,
                # receive_date    = receive_date,
                quantity        = request['quantity'],
                status_id       = request['status_id']
            )
            db.session.add(data)
        else:
            data.item           = request['item']
            # data.expiry_date     = expiry_date
            # data.receive_date    = receive_date
            data.quantity       = request['quantity']
            data.status_id      = request['status_id']

        db.session.commit()

        return True

    def deleteInventory(request):

        data = Inventory.query.filter_by(id=request['id']).first()
        
        if data == None:
            return False
        else:
            db.session.delete(data)
            db.session.commit()
            return True

    # ==================================================================================
    # ROLES

    def readRoles():
        return Roles.query.all()

    def readRole(id):
        return Roles.query.filter_by(id=id).first()

    def upsertRole(request):

        data = Roles.query.filter_by(id=request['id']).first()

        if data == None:
            data = Roles(
                role  = request['role']
            )
            db.session.add(data)
        else:
            data.role  = request['role']

        db.session.commit()

        return True

    def deleteRole(request):

        data = Roles.query.filter_by(id=request['id']).first()

        if data == None:
            return False
        else:
            db.session.delete(data)
            db.session.commit()
            return True

    # ==================================================================================
    # SERVICE

    def readServices():
        return Services.query.all()

    def readService(id):
        return Services.query.filter_by(id=id).first()

    def upsertService(request):

        data = Services.query.filter_by(id=request['id']).first()

        if data == None:
            data = Services(
                service         = request['service'],
                availability    = request['availability']
            )
            db.session.add(data)
        else:
            data.service        = request['service']
            data.availability   = request['availability']

        db.session.commit()

        return True

    def deleteService(request):

        data = Services.query.filter_by(id=request['id']).first()

        if data == None:
            return False
        else:
            db.session.delete(data)
            db.session.commit()
            return True

    # ==================================================================================
    # STATUS

    def readAllStatus():
        return Status.query.all()

    def readStatus(id):
        return Status.query.filter_by(id=id).first()

    def upsertStatus(request):

        data = Status.query.filter_by(id=request['id']).first()

        if data == None:
            data = Status(
                status  = request['status']
            )
            db.session.add(data)
        else:
            data.status  = request['status']

        db.session.commit()

        return True

    def deleteStatus(request):

        data = Status.query.filter_by(id=request['id']).first()

        if data == None:
            return False
        else:
            db.session.delete(data)
            db.session.commit()
            return True

    # ==================================================================================
    # NOTIFICATIONS

    def sendSMS(number, msg):
        # code for sms notifications here
        pass

    def sendEmail(request):
        # code for email notifications here
        pass

    def updateNotification(id):
        data = Notifications.query.filter_by(id=id).first()
        data.viewed = True
        db.session.commit()
        return True

    def readAccountNotifications(id):
        data = Notifications.query.filter_by(account_id=id).all()
        return data

    def readNotification(id):
        data = Notifications.query.filter_by(id=id).first()
        return data

    def readAllNotifications():
        data = Notifications.query.all()
        return data

# =============================================================================================

    def populate():

        # create roles

        role = Roles(role='admin')
        db.session.add(role)

        role = Roles(role='staff')
        db.session.add(role)

        role = Roles(role='patient')
        db.session.add(role)

        # create status

        status = Status(status='Approved')
        db.session.add(status)

        status = Status(status='Declined')
        db.session.add(status)

        status = Status(status='Cancelled')
        db.session.add(status)

        status = Status(status='Pending')
        db.session.add(status)

        status = Status(status='Available')
        db.session.add(status)

        status = Status(status='Used')
        db.session.add(status)

        status = Status(status='Expired')
        db.session.add(status)

        # create accounts

        account = Accounts(
            first_name  = 'System',
            middle_name = '',
            last_name   = 'Administrator',
            gender      = '',
            civil       = '',
            phone       = '+639354796747',
            birth_date  = '',
            address     = 'CDO',
            email       = 'admin@gmail.com',
            password    = 'admin1234',
            occupation    = 'Barangay Health Worker',
            role_id     = 1
        )
        db.session.add(account)

        account = Accounts(
            first_name  = 'Sample',
            middle_name = '',
            last_name   = 'Patient',
            gender      = '',
            civil       = '',
            phone       = '+639354796747',
            birth_date  = '',
            address     = 'CDO',
            email       = 'patient@gmail.com',
            password    = 'admin1234',
            occupation    = '',
            role_id     = 3
        )
        db.session.add(account)

        # create service

        service = Services(
            service  = 'Immunize'
        )
        db.session.add(service)

        db.session.commit()

        return True    