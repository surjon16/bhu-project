from data import db
from data import login_manager
from flask_login import UserMixin
import re 
from werkzeug.security import generate_password_hash, check_password_hash

RecordPatients = db.Table('record_patients',
    db.Column('account_id', db.Integer, db.ForeignKey('accounts.id')),
    db.Column('record_id', db.Integer, db.ForeignKey('records.id'))
)

class Accounts(UserMixin, db.Model):

    id          = db.Column(db.Integer, primary_key=True)
    first_name  = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    last_name   = db.Column(db.String(100))
    gender      = db.Column(db.String(10))
    civil       = db.Column(db.String(10))
    phone       = db.Column(db.String(15))
    birth_date  = db.Column(db.DateTime)
    address     = db.Column(db.String(100))
    position    = db.Column(db.String(100))

    # login
    email           = db.Column(db.String(100))
    password_hash   = db.Column(db.String(128))

    # timestamps
    login_date  = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    role_id                 = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    account_notifications   = db.relationship('Notifications', backref='account', lazy=True)
    record_patient    = db.relationship('Records', secondary=RecordPatients,  backref=db.backref('patient', uselist=False),  lazy='dynamic')

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return {
            'id'            : self.id,
            'first_name'    : self.first_name,
            'middle_name'   : self.middle_name,
            'last_name'     : self.last_name,
            'gender'        : self.gender,
            'civil'         : self.civil,
            'phone'         : self.phone,
            'birth_date'    : self.birth_date.strftime('%m/%d/%Y') if self.birth_date is not None else None,
            'email'         : self.email,
            'created_at'    : self.created_at,
            'updated_at'    : self.updated_at,
            'address'       : self.address,
            'position'      : self.position,
            'role_id'       : self.role_id
        }

class Records(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    case_number     = db.Column(db.String(100))
    case_title      = db.Column(db.String(100))
    location        = db.Column(db.String(100))
    respondent      = db.Column(db.String(100))
    narrative       = db.Column(db.Text)
    date_reported   = db.Column(db.DateTime)
    date_record   = db.Column(db.DateTime)

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    status_id   = db.Column(db.Integer, db.ForeignKey('status.id'),     nullable=True)

    records_appointments = db.relationship('Appointments', backref='record', lazy=True)

    def __str__(self):
        return {
            'id'            : self.id,
            'case_number'   : self.case_number,
            'case_title'    : self.case_title,
            'location'      : self.location,
            'narrative'     : self.narrative,
            'date_reported' : self.date_reported.strftime('%Y-%m-%dT%H:%M') if self.date_reported is not None else None,
            'date_record' : self.date_record.strftime('%Y-%m-%dT%H:%M') if self.date_record is not None else None,
            'created_at'    : self.created_at,
            'updated_at'    : self.updated_at,
            'status_id'     : self.status.id,
            'current_status': self.status.status,
            'patient_id': self.patient.id,
            'patient'   : self.patient.first_name + ' ' + self.patient.last_name,
            'respondent'    : self.respondent
        }
    
class Appointments(db.Model):

    id          = db.Column(db.Integer, primary_key=True)
    details     = db.Column(db.Text)
    appointment    = db.Column(db.DateTime)
    lupon       = db.Column(db.JSON)
    minutes     = db.Column(db.Text)

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'),  nullable=True)
    
    def __str__(self):
        return {
            'id'                    : self.id,
            'details'               : self.details,
            'appointment'              : self.appointment.strftime('%Y-%m-%dT%H:%M') if self.appointment is not None else None,
            'record_id'           : self.record_id,
            'record_status'       : self.record.status.status,
            'record_status_id'    : self.record.status.id,
            'minutes'               : self.minutes,
            'case_title'            : self.record.case_title,
            'lupon'                 : self.lupon
        }

class Roles(db.Model):

    id      = db.Column(db.Integer, primary_key=True)
    role    = db.Column(db.String(20))

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    accounts_roles = db.relationship('Accounts', backref='role', lazy=True)

    def __str__(self):
        return {
            'id'            : self.id,
            'role'          : self.role,
            'created_at'    : self.created_at,
            'updated_at'    : self.updated_at
        }
    
class Status(db.Model):

    id      = db.Column(db.Integer, primary_key=True)
    status  = db.Column(db.String(50))

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    records_status = db.relationship('Records', backref='status', lazy=True)

    def __str__(self):
        return {
            'id'            : self.id,
            'status'        : self.status,
            'created_at'    : self.created_at,
            'updated_at'    : self.updated_at
        }

class Notifications(db.Model):

    id          = db.Column(db.Integer, primary_key=True)
    content     = db.Column(db.Text)
    notif_type  = db.Column(db.String(20))
    viewed      = db.Column(db.Boolean, default=False)

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'),     nullable=True)

    def __str__(self):
        return {
            'id'            : self.id,
            'content'       : self.content,
            'account_id'    : self.account.id,
            'viewed'        : self.viewed,
            'notif_type'    : self.notif_type,
            'created_at'    : self.created_at,
            'updated_at'    : self.updated_at
        }
    
# class RecordType(db.Model):

#     id = db.Column(db.Integer, primary_key=True)

#     # relationship
#     records_types = db.relationship('records', backref='type', lazy=True)


# ============================================================================================
@login_manager.user_loader
def load_user(id):
    return Accounts.query.get(int(id))
