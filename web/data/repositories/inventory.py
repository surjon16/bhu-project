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

class InventoryRepo:
    
    # ==================================================================================
    # INVENTORY

    def readInventories():
        return Inventory.query.all()

    def readInventory(id):
        return Inventory.query.filter_by(id=id).first()

    def upsertInventory(request):

        data = Inventory.query.filter_by(id=request['id']).first()

        if data == None:
            data = Inventory(
                item_code       = request['item_code'],
                item            = request['item'],
                min_quantity    = request['min_quantity'],
                max_quantity    = request['max_quantity'],
                reorder_level   = request['reorder_level']
            )
            db.session.add(data)
        else:
            data.item_code      = request['item_code']
            data.item           = request['item']
            data.min_quantity   = request['min_quantity']
            data.max_quantity   = request['max_quantity']
            data.reorder_level  = request['reorder_level']

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
