from flask          import jsonify, render_template, request, redirect, url_for, make_response
from application    import app
from data.repo      import Repository
from data.schemas   import CreateAccountSchema, UpdateAccountSchema, CreateRecordSchema, CreateAppointmentSchema, CreateServiceSchema, CreateInventorySchema, AddItemsSchema
import json

# API RESOURCE PATTERN

# GET         /data/get/<id>    get data data by id
# GET         /data/get/all     get data list
# POST        /data/upsert/     upsert data
# POST        /data/delete/     delete data

# ==================================================================================
# ACCOUNTS

@app.route('/api/account/get/<id>', methods=['GET'])
def get_account(id):
    return jsonify(Repository.readAccount(id).serialize())

@app.route('/api/account/get/all', methods=['GET'])
def get_all_accounts():
    return jsonify([data.serialize() for data in Repository.readAccounts()])

@app.route('/api/account/upsert', methods=['POST'])
def upsert_account():

    if int(request.form['id']) == -1:
        validator = CreateAccountSchema(unknown='EXCLUDE')
        errors = validator.validate(request.form)
        if errors:
            return jsonify({'success':False, 'errors':errors})
    else:
        validator = UpdateAccountSchema(unknown='EXCLUDE')
        errors = validator.validate(request.form)
        if errors:
            return jsonify({'success':False, 'errors':errors})

    if Repository.upsertAccount(request.form):
        return {'success':True}
    return {'success':True}

@app.route('/api/account/delete', methods=['POST'])
def delete_account():
    if Repository.deleteAccount(request.form):
        return {'success':True}
    return {'success':False}


# ==================================================================================
# RECORDS

@app.route('/api/record/get/<id>', methods=['GET'])
def get_record(id):
    return jsonify(Repository.readRecord(id).serialize())

@app.route('/api/record/get/all', methods=['GET'])
def get_all_records():
    return jsonify([data.serialize() for data in Repository.readRecords()])

@app.route('/api/record/upsert', methods=['POST'])
def upsert_record():
    
    validator = CreateRecordSchema(unknown='EXCLUDE')
    errors = validator.validate(request.form)

    if errors:
        return jsonify({'success':False, 'errors':errors})

    if Repository.upsertRecord(request.form):
        return {'success':True}
    return {'success':False}

@app.route('/api/record/delete', methods=['POST'])
def delete_record():
    if Repository.deleteRecord(request.form):
        return {'success':True}
    return {'success':False}


# ==================================================================================
# APPOINTMENTS

@app.route('/api/appointment/get/<id>', methods=['GET'])
def get_appointment(id):
    return jsonify(Repository.readAppointment(id).serialize())

@app.route('/api/appointment/get/daily', methods=['GET'])
def get_daily_appointments():
    return jsonify(Repository.readInventoriesGroupByItem())
    return jsonify([data.serialize() for data in Repository.readInventoriesGroupByItem()])

@app.route('/api/appointment/get/all', methods=['GET'])
def get_all_appointments():
    return jsonify([data.serialize() for data in Repository.readAppointments()])

@app.route('/api/appointment/get/schedules', methods=['GET'])
def get_scheduled_appointments():
    return jsonify(Repository.readSchedules())

@app.route('/api/appointment/get/slots', methods=['GET'])
def get_slots_appointments():
    return jsonify(Repository.readAvailableSlots())

@app.route('/api/appointment/upsert', methods=['POST'])
def upsert_appointment():
    
    validator = CreateAppointmentSchema(unknown='EXCLUDE')
    errors = validator.validate(request.form)

    if errors:
        return jsonify({'success':False, 'errors':errors})

    if Repository.upsertAppointment(request.form):
        return {'success':True}
    return {'success':False}

@app.route('/api/appointment/delete', methods=['POST'])
def delete_appointment():
    if Repository.deleteAppointment(request.form):
        return {'success':True}
    return {'success':False}

# ==================================================================================
# INVENTORY

@app.route('/api/inventory/get/<id>', methods=['GET'])
def get_inventory(id):
    return jsonify(Repository.readInventory(id).serialize())

@app.route('/api/inventory/get/all', methods=['GET'])
def get_all_inventory():
    return jsonify([data.serialize() for data in Repository.readInventories()])

@app.route('/api/inventory/upsert', methods=['POST'])
def upsert_inventory():
    
    validator = CreateInventorySchema(unknown='EXCLUDE')
    errors = validator.validate(request.form)

    if errors:
        return jsonify({'success':False, 'errors':errors})

    if Repository.upsertInventory(request.form):
        return {'success':True}
    return {'success':False}

@app.route('/api/inventory/items/upsert', methods=['POST'])
def upsert_inventory_items():
    
    validator = AddItemsSchema(unknown='EXCLUDE')
    errors = validator.validate(request.form)

    if errors:
        return jsonify({'success':False, 'errors':errors})

    if Repository.upsertItems(request.form):
        return {'success':True}
    return {'success':False}

@app.route('/api/inventory/delete', methods=['POST'])
def delete_inventory():
    if Repository.deleteInventory(request.form):
        return {'success':True}
    return {'success':False}

# ==================================================================================
# ROLES

@app.route('/api/role/get/<id>', methods=['GET'])
def get_role(id):
    return jsonify(Repository.readRole(id).serialize())

@app.route('/api/role/get/all', methods=['GET'])
def get_all_roles():
    return jsonify([data.serialize() for data in Repository.readRoles()])

@app.route('/api/role/upsert', methods=['POST'])
def upsert_role():
    if Repository.upsertRole(request.form):
        return {'success':True}
    return {'success':False}

@app.route('/api/role/delete', methods=['POST'])
def delete_role():
    if Repository.deleteRole(request.form):
        return {'success':True}
    return {'success':False}

# ==================================================================================
# SERVICES

@app.route('/api/service/get/<id>', methods=['GET'])
def get_service(id):
    return jsonify(Repository.readService(id).serialize())

@app.route('/api/service/get/all', methods=['GET'])
def get_services():
    return jsonify([data.serialize() for data in Repository.readServices()])

@app.route('/api/service/upsert', methods=['POST'])
def upsert_service():
    
    validator = CreateServiceSchema(unknown='EXCLUDE')
    errors = validator.validate(request.form)

    if errors:
        return jsonify({'success':False, 'errors':errors})

    if Repository.upsertService(request.form):
        return {'success':True}
    return {'success':False}

@app.route('/api/service/delete', methods=['POST'])
def delete_service():
    if Repository.deleteService(request.form):
        return {'success':True}
    return {'success':False}

# ==================================================================================
# STATUS

@app.route('/api/status/get/<id>', methods=['GET'])
def get_status(id):
    return jsonify(Repository.readStatus(id).serialize())

@app.route('/api/status/get/all', methods=['GET'])
def get_all_status():
    return jsonify([data.serialize() for data in Repository.readAllStatus()])

@app.route('/api/status/upsert', methods=['POST'])
def upsert_status():
    if Repository.upsertStatus(request.form):
        return {'success':True}
    return {'success':False}

@app.route('/api/status/delete', methods=['POST'])
def delete_status():
    if Repository.deleteStatus(request.form):
        return {'success':True}
    return {'success':False}

# ==================================================================================
# NOTIFICATIONS

@app.route('/api/notifications/sms/send', methods=['GET'])
def send_sms():
    response = Repository.sendSMS()
    return jsonify(response)
    
@app.route('/api/notifications/get/all', methods=['GET'])
def get_all_notifications():
    return jsonify([data.serialize() for data in Repository.readAllNotifications()])

@app.route('/api/notifications/account/get/<id>', methods=['GET'])
def get_account_notifications(id):
    return jsonify([data.serialize() for data in Repository.readAccountNotifications(id)])

@app.route('/api/notifications/get/<id>', methods=['GET'])
def get_notification(id):
    return jsonify(Repository.readNotification(id).serialize())

@app.route('/api/notifications/update/<id>', methods=['GET'])
def update_notification(id):
    if Repository.updateNotification(id):
        return {'success':True}
    return {'success':False}

# ==================================================================================
# FACTORY

@app.route('/api/populate', methods=['GET'])
def populate():
    Repository.populate()
    return {'success':True}

@app.route('/api/tester', methods=['GET'])
def tester():
    return jsonify(Repository.readSchedules())    