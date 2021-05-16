from flask          import flash, jsonify, render_template, request, redirect, url_for, session
from flask_login    import login_required, login_user, logout_user, current_user
from application    import app
from data.repo      import Repository
from data.schemas   import RegisterAccountSchema
from datetime       import datetime, timedelta
from functools      import wraps
import dateutil.parser as parser

# ===============================================================
# DECORATORS
# ===============================================================

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    date = parser.parse(date)
    native = date.replace(tzinfo=None)
    format='%m/%d/%Y'
    return native.strftime(format)

@app.context_processor
def inject_now():
    return {
        'now'   : datetime.now(),
        'day'   : timedelta(days=1),
        'month' : timedelta(days=30),
        'time_schedules' : [
            {'v': 9,  't':'09:00AM-10:00AM'},
            {'v': 10, 't':'10:00AM-11:00AM'},
            {'v': 11, 't':'11:00AM-12:00NN'},
            {'v': 13, 't':'01:00PM-02:00PM'},
            {'v': 14, 't':'02:00PM-03:00PM'},
            {'v': 15, 't':'03:00PM-04:00PM'},
            {'v': 16, 't':'04:00PM-05:00PM'}
        ]
    }

def admin_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if current_user.role_id is None:
            return redirect(url_for('patient_dashboard'))
            
        if current_user.role_id == 3:
            return redirect(url_for('patient_dashboard'))

        return f(*args, **kwargs)
    return wrapper
       
def patient_login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        if current_user.role_id == 1:
            return redirect(url_for('dashboard'))

        # if current_user.role_id == 2:
        #     return redirect(url_for('dashboard'))
            
        return f(*args, **kwargs)
    return wrapper
       

# ===============================================================
# WEB VIEWS
# ===============================================================
 
@app.route('/')
@login_required
def home():
    return redirect(url_for('dashboard'))

@app.route('/admin/dashboard')
@login_required
@admin_login_required
def dashboard():
    response = {
        'accounts'  : Repository.readRegisteredAccounts(),
        'records' : Repository.readRecords(),
        'appointments' : Repository.readAppointments()
    }
    return render_template('admin/dashboard.html', data=response)

@app.route('/admin/records')
@login_required
@admin_login_required
def records():
    response = {
        'roles'         : Repository.readRoles(),
        'status'        : Repository.readAllStatus(),
        'services'      : Repository.readServices(),
        'accounts'      : Repository.readAccounts(),
        'residents'     : Repository.readResidentAccounts(),
        'records'       : Repository.readRecords(),
        'appointments'  : Repository.readDailyAppointments(datetime.now().strftime('%m/%d/%Y')),
        'inventories'   : Repository.readInventories(),
        'current_date'  : datetime.now(),
        'form'          : None
    }
    return render_template('admin/records.html', data=response)

@app.route('/admin/record/<id>')
@login_required
@admin_login_required
def record(id):
    response = {
        'record' : Repository.readRecord(id)
    }
    return render_template('admin/record.html', data=response)

@app.route('/admin/records/search', methods=['POST', 'GET'])
@login_required
@admin_login_required
def search_records():
    if request.method == 'POST':
        date = request.form['start_date']
        response = {
            'roles'         : Repository.readRoles(),
            'status'        : Repository.readAllStatus(),
            'services'      : Repository.readServices(),
            'accounts'      : Repository.readAccounts(),
            'residents'     : Repository.readResidentAccounts(),
            'records'       : Repository.readRecords(),
            'appointments'  : Repository.searchAppointments(request.form),
            'inventories'   : Repository.readInventories(),
            'current_date'  : datetime.strptime(date, '%m/%d/%Y'),
            'form'          : request.form
        }
        return render_template('admin/records.html', data=response)

@app.route('/admin/appointments')
@login_required
@admin_login_required
def appointments():
    response = {
        'roles'         : Repository.readRoles(),
        'status'        : Repository.readAllStatus(),
        'services'      : Repository.readServices(),
        'accounts'      : Repository.readAccounts(),
        'residents'     : Repository.readResidentAccounts(),
        'records'       : Repository.readRecords(),
        'appointments'  : Repository.readDailyAppointments(datetime.now().strftime('%m/%d/%Y')),
        'inventories'   : Repository.readInventories(),
        'current_date'  : datetime.now(),
        'form'          : None
    }
    return render_template('admin/appointments.html', data=response)

@app.route('/admin/appointment/<id>')
@login_required
@admin_login_required
def appointment(id):
    response = {
        'appointment' : Repository.readAppointment(id)
    }
    return render_template('admin/appointment.html', data=response)

@app.route('/admin/appointment/search', methods=['POST', 'GET'])
@login_required
@admin_login_required
def search_appointments():
    if request.method == 'POST':
        date = request.form['start_date']
        response = {
            'roles'         : Repository.readRoles(),
            'status'        : Repository.readAllStatus(),
            'services'      : Repository.readServices(),
            'accounts'      : Repository.readAccounts(),
            'residents'     : Repository.readResidentAccounts(),
            'records'       : Repository.readRecords(),
            'appointments'  : Repository.searchAppointments(request.form),
            'inventories'   : Repository.readInventories(),
            'current_date'  : datetime.strptime(date, '%m/%d/%Y'),
            'form'          : request.form
        }
        return render_template('admin/appointments.html', data=response)

    return redirect(url_for('appointments'))

@app.route('/admin/residents')
@login_required
@admin_login_required
def residents():
    response = {
        'result'    : Repository.readResidentAccounts(),
        'accounts'  : Repository.readResidentAccounts()
    }
    return render_template('admin/residents.html', data=response)

@app.route('/admin/resident/<id>')
@login_required
@admin_login_required
def resident(id):
    response = Repository.readAccount(id)
    return render_template('admin/resident.html', data=response)

@app.route('/admin/residents/search', methods=['POST', 'GET'])
@login_required
@admin_login_required
def search_residents():
    if request.method == 'POST':
        account_id = int(request.form['account_id'])
        if account_id == -1:
            return redirect(url_for('residents'))

        response = {
            'result'    : [Repository.readAccount(account_id)],
            'accounts'  : Repository.readResidentAccounts()
        }
        return render_template('admin/residents.html', data=response)

@app.route('/admin/accounts')
@login_required
@admin_login_required
def accounts():
    response = Repository.readAccounts()
    return render_template('admin/accounts.html', data=response)

@app.route('/admin/account/<id>')
@login_required
@admin_login_required
def account(id):
    response = Repository.readAccount(id)
    return render_template('admin/account.html', data=response)

@app.route('/admin/inventories')
@login_required
@admin_login_required
def inventories():
    response = {
        'status'        : Repository.readAllStatus(),
        'inventories'   : Repository.readInventories(),
        'current_date'  : datetime.now()
    }
    return render_template('admin/inventories.html', data=response)

@app.route('/admin/inventory/<id>')
@login_required
@admin_login_required
def inventory(id):
    response = {
        'inventory' : Repository.readInventory(id),
        'current_date'  : datetime.now()
    }
    return render_template('admin/inventory.html', data=response)

@app.route('/admin/inventories/search', methods=['POST', 'GET'])
@login_required
@admin_login_required
def search_inventories():
    if request.method == 'POST':
        category = int(request.form['category'])
        if category == -1:
            return redirect(url_for('inventories'))

        response = {
            'status'        : Repository.readAllStatus(),
            'inventories'   : [Repository.readInventory(category)],
            'current_date'  : datetime.now()
        }
        return render_template('admin/inventories.html', data=response)

@app.route('/admin/services')
@login_required
@admin_login_required
def services():
    response = {
        'services' : Repository.readServices()
    }
    return render_template('admin/services.html', data=response)

@app.route('/admin/settings')
@login_required
@admin_login_required
def settings():
    response = {
        'roles' : Repository.readRoles(),
        'status' : Repository.readAllStatus()
    }
    return render_template('admin/settings.html', data=response)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = Repository.loginAccount(request.form)
        if data is not None and data is not False:
            if data.role_id is not None:
                if data.role_id < 3 and data.occupation != 'Barangay Lupon':
                    return redirect(url_for('dashboard'))        
            return redirect(url_for('patient_dashboard'))
        else:
            flash('Invalid credentials.')
    return render_template('common/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        validator = RegisterAccountSchema(unknown='EXCLUDE')
        errors = validator.validate(request.form)

        if errors:
            return render_template('common/register.html', data={'errors': errors, 'input': request.form})

        if Repository.registerAccount(request.form):
            return redirect(url_for('login'))

    return render_template('common/register.html', data={'errors':[], 'input': []})


# ===============================================================
# MOBILE VIEWS
# ===============================================================

@app.route('/patient/dashboard')
@login_required
@patient_login_required
def patient_dashboard():
    response = {
        'notifications' : Repository.readAllNotifications(),
        'accounts'      : Repository.readAccounts(),
        'records'       : Repository.readRecords(),
        'appointments'  : Repository.readAppointments()
    }
    return render_template('patient/dashboard.html', data=response)

@app.route('/patient/appointments')
@login_required
@patient_login_required
def patient_appointments():
    response = {
        'notifications' : Repository.readAllNotifications(),
        'roles'         : Repository.readRoles(),
        'status'        : Repository.readAllStatus(),
        'accounts'      : Repository.readAccounts(),
        'records'       : Repository.readRecords(),
        'appointments'  : Repository.readAppointments()
    }
    return render_template('patient/appointments.html', data=response)

@app.route('/patient/appointment/details/<id>')
@login_required
@patient_login_required
def patient_appointment_details(id):
    response = {
        'appointment'   : Repository.readAppointment(id)
    }
    return render_template('patient/appointment_details.html', data=response)

@app.route('/patient/record/details/<id>')
@login_required
@patient_login_required
def patient_record_details(id):
    response = {
        'appointment'   : Repository.readAppointment(id)
    }
    return render_template('patient/record_details.html', data=response)

@app.route('/patient/appointment/request')
@login_required
@patient_login_required
def patient_appointment_request():
    response = {
        'status'        : Repository.readAllStatus(),
        'services'      : Repository.readServices(),
        'appointments'  : Repository.readAppointments(),
        'schedules'     : Repository.readSchedules(),
        'current_date'  : datetime.now()
    }
    return render_template('patient/appointment_request.html', data=response)

@app.route('/patient/notifications')
@login_required
@patient_login_required
def patient_notifications():
    response = {
        'notifications' : Repository.readAllNotifications()
    }
    return render_template('patient/notifications.html', data=response)

@app.route('/patient/notification/<id>')
@login_required
@patient_login_required
def patient_notification(id):
    Repository.updateNotification(id)
    response = {
        'notifications' : Repository.readAllNotifications(),
        'notification' : Repository.readNotification(id)
    }
    return render_template('patient/notification.html', data=response)
