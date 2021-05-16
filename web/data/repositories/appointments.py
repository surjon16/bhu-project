from data.models    import Accounts, Roles, Inventory, Appointments, Status, Notifications, Services, Items
from data           import db

from flask_login    import login_user, current_user
from sqlalchemy     import extract, or_, and_, func
from sqlalchemy.sql import label
from datetime       import datetime, timedelta

import requests, json
import os

itexmo_hdr = {'content-type': 'application/x-www-form-urlencoded'}
itexmo_url = "https://www.itexmo.com/php_api/api.php"
itexmo_api = 'ST-LEONE670607_8GLTB1'
itexmo_pwd = 'm6}}ktrp{{'

max_slots = 2 # slots per hour from 9AM to 5PM
daily_slots = 14 # for 7hours at max slots per hour

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

    def readAvailableSlots():

        appointments = db.session.query(Appointments.appointment_date).filter(or_(Appointments.status_id==1, Appointments.status_id==4)).all()
        data = appointments if appointments is not None else []

        daily = [i.appointment_date.strftime('%m/%d/%Y') for i in data]
        dailylist = list(set(daily))

        hourly = [i.appointment_date for i in data]
        hourlylist = list(set(hourly))
        hourlydata = [{
            'dt': h,
            'd' : h.strftime('%m/%d/%Y'),
            'h' : h.strftime('%I:%M%p') + '-' + (h + timedelta(hours=1)).strftime('%I:%M%p')
        } for h in hourlylist]        
        
        return [{
            'slots' : daily_slots - daily.count(i),
            'date'  : i,
            'time'  : [{
                't' : t['h'],
                'slots' : max_slots - hourly.count(t['dt'])
            } for t in hourlydata if t['d'] == i]
        } for i in dailylist]

    def readSchedules():

        appointments = db.session.query(Appointments.appointment_date).filter(or_(Appointments.status_id==1, Appointments.status_id==4)).all()
        datalist = list(set(appointments if appointments is not None else []))

        schedules = [{
                'datetime' : data.appointment_date,
                'date': data.appointment_date.strftime('%m/%d/%Y'), 
                'time': data.appointment_date.strftime('%I:%M%p') + '-' + (data.appointment_date + timedelta(hours=1)).strftime('%I:%M%p'),
                'slots': max_slots - appointments.count(data)
            } for data in datalist]

        return schedules

    def searchAppointments(request):

        start_date  = datetime.strptime(request['start_date'], '%m/%d/%Y').strftime('%Y-%m-%d') if request['start_date'] is not None else None
        end_date    = (datetime.strptime(request['end_date'], '%m/%d/%Y') + timedelta(days=1)).strftime('%Y-%m-%d') if request['end_date'] is not None else None
        patient     = int(request['patient'])
        service     = int(request['service'])
        status      = int(request['status'])

        data = db.session.query(Appointments).filter(Appointments.appointment_date >= start_date).filter(Appointments.appointment_date <= end_date)
        
        if patient > -1: data = data.filter(Appointments.account_id==patient)
        if service > -1: data = data.filter(Appointments.service_id==service)
        if status  > -1: data = data.filter(Appointments.status_id==status)

        return data.all()
        

    def updateAppointmentStatus(request):

        data = Appointments.query.filter_by(id=request['id']).first()
        data.status_id = request['status_id']

        db.session.commit()

        return True

    def upsertAppointment(request):

        data = Appointments.query.filter_by(id=request['id']).first()

        appointment_date = request['appointment_date']
        try:
            appointment_date = datetime.strptime(appointment_date, '%m/%d/%Y') + timedelta(hours=int(request['time']))
        except ValueError:
            appointment_date = request['appointment_date']

        if data == None:
            data = Appointments(
                details             = request['details'],
                appointment_date    = appointment_date,
                assigned            = request['assigned'],
                account_id          = request['account_id'],
                service_id          = request['service_id'],
                status_id           = request['status_id']
            )
            db.session.add(data)

        else:

            data.details             = request['details']
            data.appointment_date    = appointment_date
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

        # try:
            
        #     # Send an sms to the patient.
        #     sms = {
        #         '1'         : data.account.phone,
        #         '2'         : content,
        #         '3'         : 'ST-LEONE670607_8GLTB',
        #         'passwd'    : 'm6}}ktrp{{'
        #     }
        #     response = requests.post(url=itexmo_url, data=sms)
        #     print(response.text)

        # except:
            
        #     return True

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

    def tester():
        pass
