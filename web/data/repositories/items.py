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

class ItemsRepo:

    def readItems():
        return Items.query.all()

    def readItem(request):
        return Items.query.filter_by(id=request['id']).first()
    
    def upsertItems(request):
        
        expiry_date     = request['expiry_date']
        inventory_id    = request['inventory_id']
        status_id       = request['status_id']

        try:
            expiry_date = datetime.strptime(expiry_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            expiry_date = None

        for x in range(int(request['quantity'])):
            data = Items(
                inventory_id    = inventory_id,
                expiry_date     = expiry_date,
                status_id       = status_id
            )
            db.session.add(data)
            db.session.commit()

        return True

    def upsertItem(request):

        data = Items.query.filter_by(id=request['id']).first()

        expiry_date = request['expiry_date']
        try:
            expiry_date = datetime.strptime(expiry_date, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            expiry_date = None

        if data == None:
            data = Items(
                inventory_id    = request['inventory_id'],
                expiry_date     = expiry_date,
                status_id       = request['status_id']
            )
            db.session.add(data)
        else:
            data.inventory_id   = request['inventory_id']
            data.expiry_date    = expiry_date
            data.status_id      = request['status_id']

        db.session.commit()

        return True


