from data.models    import Accounts, Roles, Records, Appointments, Status, Notifications
from data           import db

from flask_login    import login_user, current_user
from sqlalchemy     import extract, or_, and_
from datetime       import datetime

import requests, json
import os

from twilio.rest                import Client
from twilio.http.http_client    import TwilioHttpClient

# proxy_client = TwilioHttpClient()
# proxy_client.session.proxies = {'https': os.environ['https_proxy']}

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
    
    def readLuponAccounts():
        return Accounts.query.filter(and_(Accounts.role_id==2, Accounts.position == 'Barangay Lupon')).all()
    
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
                    position    = request['position'],
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
                    position    = request['position'],
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
            data.position    = request['position']
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

            # delete all filed cases
            for record in data.record_patient:

                # delete all appointments
                for appointment in record.records_appointments:
                    db.session.delete(appointment)
                
                db.session.delete(record)

            # finally, delete account
            db.session.delete(data)
            db.session.commit()

            return True

    # ==================================================================================
    # INCIDENTS
    
    def readRecords():
        return Records.query.all()

    def readMonthlyRecords(date):
        data = Records.query.filter(extract('year', Records.date_reported) == int(date[0:4]), extract('month', Records.date_reported) == int(date[5:])).all()
        return data

    def readRecord(id):
        return Records.query.filter_by(id=id).first()
    
    def upsertRecord(request):

        data = Records.query.filter_by(id=request['id']).first()

        if data == None:

            data = Records(
                case_number     = request['case_number'],
                case_title      = request['case_title'],
                location        = request['location'],
                narrative       = request['narrative'],
                date_reported   = request['date_reported'],
                date_record   = request['date_record'],
                respondent      = request['respondent'],
                status_id       = request['status_id']
            )

            db.session.add(data)

            if request['patient'] is not None:  data.patient = Accounts.query.filter_by(id=request['patient']).first()

        else:

            data.case_number    = request['case_number']
            data.case_title     = request['case_title']
            data.location       = request['location']
            data.narrative      = request['narrative']
            data.respondent     = request['respondent']
            data.date_reported  = request['date_reported']
            data.date_record  = request['date_record']
            data.status_id      = request['status_id']

            if request['patient'] is not None:  data.patient = Accounts.query.filter_by(id=request['patient']).first()

        db.session.commit()

        return True

    def updateRecordStatus(request):

        data = Records.query.filter_by(id=request['id']).first()

        if data == None:
            return False
        else:
            data.status_id = request['status_id']
            db.session.commit()
            return True


    def deleteRecord(request):

        data = Records.query.filter_by(id=request['id']).first()

        if data == None:
            return False
        else:
            
            # delete all appointments
            for appointment in data.records_appointments:
                db.session.delete(appointment)
            
            db.session.delete(data)
            db.session.commit()
            
            return True

    # ==================================================================================
    # SCHEDULES
    
    def readAppointments():
        return Appointments.query.all()
    
    def readAppointment(id):
        return Appointments.query.filter_by(id=id).first()

    def upsertAppointment(request):

        data = Appointments.query.filter_by(id=request['id']).first()

        if data == None:
            data = Appointments(
                details     = request['details'],
                appointment    = request['appointment'],
                record_id = request['record_id'],
                lupon       = request['assigned_lupon']
                # created_by  = request['created_by']
            )
            db.session.add(data)

        else:
            data.details     = request['details']
            data.appointment    = request['appointment']
            data.record_id = request['record_id']
            # data.created_by  = request['created_by']
            data.lupon       = request['assigned_lupon']
                
        db.session.commit()

        # =============================================================================================================
        # Create a notification after creating a appointment
        content = request['details']
        notifs = Notifications(content=content, notif_type='app', account_id=data.record.patient.id)
        db.session.add(notifs)
        db.session.commit()

        # Set account details
        # account_sid = 'AC9d6e97214085f5b8a7e31001dd8a0ba1'
        # client = Client(account_sid, auth_token, http_client=proxy_client)
        # client = Client(account_sid, auth_token)
        
        try:
            
            # Send an sms to the patient.
            # message = client.messages.create(
            #     body=content,
            #     from_='+17542192549', 
            #     to=data.record.patient.phone
            # )
            
            sms = {
                '1'         : data.record.patient.phone,
                '2'         : content,
                '3'         : 'ST-LEONE670607_8GLTB',
                'passwd'    : 'm6}}ktrp{{'
            }
            response = requests.post(url=itexmo_url, data=sms)
            print(response.text)

            # Send an sms to the staff.
            staff = Accounts.query.filter(Accounts.role_id==2).all()
            for account in staff:

                if str(account.id) in data.lupon:

                    # Create notif for each staff
                    notifs = Notifications(content=content, notif_type='app', account_id=account.id)
                    db.session.add(notifs)
                    db.session.commit()

                    # message = client.messages.create(
                    #     body=content,
                    #     from_='+17542192549',
                    #     to=account.phone
                    # )

                    sms = {
                        '1'         : account.phone,
                        '2'         : content,
                        '3'         : 'ST-LEONE670607_8GLTB',
                        'passwd'    : 'm6}}ktrp{{'
                    }
                    response = requests.post(url=itexmo_url, data=sms)
                    print(response.text)
                    
            # =============================================================================================================
        
        except:

            return True

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
    # HEARING

    def upsertHearing(request):

        data = Appointments.query.filter_by(id=request['id']).first()

        data.minutes            = request['minutes']
        data.record.status_id = request['status_id']
                
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
            position    = 'Barangay Health Worker',
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
            position    = '',
            role_id     = 3
        )
        db.session.add(account)


        db.session.commit()

        return True    