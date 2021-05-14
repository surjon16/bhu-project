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

class AppointmentsRepo:
    
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
