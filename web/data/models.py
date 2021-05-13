from data import db
from data import login_manager
from flask_login import UserMixin
import re 
from werkzeug.security import generate_password_hash, check_password_hash

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
    occupation  = db.Column(db.String(100))

    # login
    email           = db.Column(db.String(100))
    password_hash   = db.Column(db.String(128))

    # timestamps
    login_date  = db.Column(db.DateTime, default=db.func.current_timestamp())
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    role_id                 = db.Column(db.Integer, db.ForeignKey('roles.id'),      nullable=True)
    account_notifications   = db.relationship('Notifications', backref='account',   lazy=True)
    account_appointments    = db.relationship('Appointments', backref='account',    lazy=True)

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
            'occupation'    : self.occupation,
            'role_id'       : self.role_id
        }

class Appointments(db.Model):

    # appointment info
    id                  = db.Column(db.Integer, primary_key=True)
    details             = db.Column(db.Text)
    appointment_date    = db.Column(db.DateTime)
    assigned            = db.Column(db.JSON)

    # medical record
    record_number       = db.Column(db.String(100))
    record_details      = db.Column(db.Text)
    record_date         = db.Column(db.DateTime)
    next_appointments   = db.Column(db.JSON)

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    status_id   = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True)
    service_id  = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    account_id  = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    
    def __str__(self):
        return {
            'id'                : self.id,
            'details'           : self.details,
            'appointment_date'  : self.appointment_date.strftime('%Y-%m-%dT%H:%M') if self.appointment_date is not None else None,
            'assigned'          : self.assigned,
            'account'           : self.account.first_name + ' ' + self.account.last_name,
            'record_number'     : self.record_number,
            'record_details'    : self.record_details,
            'record_date'       : self.record_date.strftime('%Y-%m-%dT%H:%M') if self.record_date is not None else None,
            'next_appointments' : self.next_appointments,
            'created_at'        : self.created_at,
            'updated_at'        : self.updated_at,
            'status'            : self.status.status,
            'service'           : self.service.service,
            'status_id'         : self.status_id,
            'account_id'        : self.account_id,
            'service_id'        : self.service_id,
        }

class Inventory(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    item            = db.Column(db.String(100))
    expiry_date     = db.Column(db.DateTime)
    receive_date    = db.Column(db.DateTime)
    quantity        = db.Column(db.Integer)
    
    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    status_id   = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True)

    def __str__(self):
        return {
            'id'            : self.id,
            'item'          : self.item,
            'quantity'      : self.quantity,
            'expiry_date'   : self.expiry_date.strftime('%m/%d/%Y') if self.expiry_date is not None else None,
            'receive_date'  : self.receive_date.strftime('%m/%d/%Y') if self.receive_date is not None else None,
            'status'        : self.status.status,
            'status_id'     : self.status.id
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
    
class Services(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    service         = db.Column(db.String(50))
    availability    = db.Column(db.Integer, default=3) # 1 for AM, 2 for PM, 3 for BOTH

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    appointment_service = db.relationship('Appointments',   backref='service', lazy=True)

    def __str__(self):
        return {
            'id'            : self.id,
            'service'       : self.service,
            'availability'  : self.availability,
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
    appointment_status  = db.relationship('Appointments',   backref='status', lazy=True)
    supply_status       = db.relationship('Inventory',      backref='status', lazy=True)

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
 
# ============================================================================================
@login_manager.user_loader
def load_user(id):
    return Accounts.query.get(int(id))
