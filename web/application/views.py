from flask          import flash, jsonify, render_template, request, redirect, url_for, session
from flask_login    import login_required, login_user, logout_user, current_user
from application    import app
from data.repo      import Repository
from data.schemas   import RegisterAccountSchema, CreateRecordSchema
from datetime       import datetime
from functools      import wraps

# ===============================================================
# DECORATORS
# ===============================================================

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

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

@app.route('/admin/reports', methods=['POST', 'GET'])
@login_required
@admin_login_required
def reports():
    if request.method == 'POST':
        date = request.form['date']
        response = {
            'date'      : date,
            'records' : Repository.readMonthlyRecords(date)
        }
        return render_template('admin/reports.html', data=response)
    
    response = {
        'date'      : datetime.now().strftime('%Y-%m'),
        'records' : Repository.readMonthlyRecords(datetime.now().strftime('%Y-%m'))
    }
    return render_template('admin/reports.html', data=response)

@app.route('/admin/print', methods=['POST', 'GET'])
@login_required
@admin_login_required
def print():
    if request.method == 'POST':
        date = request.form['date']
        response = {
            'date'      : date,
            'records' : Repository.readMonthlyRecords(date)
        }
        return render_template('admin/print.html', data=response)
    else:
        date = datetime.now
        response = {
            'date'      : date,
            'records' : Repository.readMonthlyRecords(date)
        }
        return render_template('admin/print.html', data=response)


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

@app.route('/admin/records')
@login_required
@admin_login_required
def records():
    response = {
        'roles'     : Repository.readRoles(),
        'status'    : Repository.readAllStatus(),
        'accounts'  : Repository.readAccounts(),
        'records' : Repository.readRecords()
    }
    return render_template('admin/records.html', data=response)

@app.route('/admin/record/<id>')
@login_required
@admin_login_required
def record(id):
    response = {
        'record' : Repository.readRecord(id),
        'lupon'    : Repository.readLuponAccounts()
    }
    return render_template('admin/record.html', data=response)

@app.route('/admin/appointments')
@login_required
@admin_login_required
def appointments():
    response = {
        'roles'         : Repository.readRoles(),
        'status'        : Repository.readAllStatus(),
        'accounts'      : Repository.readAccounts(),
        'lupon'         : Repository.readLuponAccounts(),
        'records'     : Repository.readRecords(),
        'appointments'     : Repository.readAppointments(),
        'current_date'  : datetime.now()
    }
    return render_template('admin/appointments.html', data=response)

@app.route('/admin/appointment/<id>')
@login_required
@admin_login_required
def appointment(id):
    response = {
        'appointment' : Repository.readAppointment(id),
        'lupon'    : Repository.readLuponAccounts()
    }
    return render_template('admin/appointment.html', data=response)

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
                if data.role_id < 3 and data.position != 'Barangay Lupon':
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
        'records'     : Repository.readRecords(),
        'appointments'     : Repository.readAppointments()
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
        'records'     : Repository.readRecords(),
        'appointments'     : Repository.readAppointments()
    }
    return render_template('patient/appointments.html', data=response)

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
