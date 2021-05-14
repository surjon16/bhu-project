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

class RolesRepo:
    
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
