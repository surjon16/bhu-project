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

class NotificationsRepo:
    
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
