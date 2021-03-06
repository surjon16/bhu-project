from data                   import db
from data                   import login_manager
from flask_login            import UserMixin
from sqlalchemy.ext.hybrid  import hybrid_property, hybrid_method
from sqlalchemy             import select, func
import re, json
from werkzeug.security      import generate_password_hash, check_password_hash
from datetime               import datetime, timedelta

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

    def serialize(self):
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
    meds                = db.Column(db.JSON)

    # medical record
    record_number       = db.Column(db.String(100))
    record_details      = db.Column(db.Text)
    record_date         = db.Column(db.DateTime)
    record_form         = db.Column(db.JSON)
    next_appointments   = db.Column(db.JSON)

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    status_id   = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True)
    service_id  = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    account_id  = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=True)
    
    @hybrid_property
    def schedule(self):
        return {
            'date': self.appointment_date.strftime('%m/%d/%Y'), 
            'time': self.appointment_date.strftime('%I:%M%p') + '-' + (self.appointment_date + timedelta(hours=1)).strftime('%I:%M%p'),
        }

    @hybrid_property
    def prescriptions(self):
        return json.loads(self.meds) if self.meds is None else json.loads(self.meds)
    
    @hybrid_property
    def form_data(self):
        return json.loads(self.service.form) if self.record_form is None else json.loads(self.record_form)
    
    def serialize(self):
        return {
            'id'                : self.id,
            'details'           : self.details,
            'appointment_date'  : self.appointment_date.strftime('%Y-%m-%dT%H:%M') if self.appointment_date is not None else None,
            'assigned'          : self.assigned,
            'account'           : self.account.first_name + ' ' + self.account.last_name,
            'record_number'     : self.record_number,
            'record_details'    : self.record_details,
            'record_form'       : self.record_form,
            'record_date'       : self.record_date.strftime('%Y-%m-%dT%H:%M') if self.record_date is not None else None,
            'next_appointments' : self.next_appointments,
            'created_at'        : self.created_at,
            'updated_at'        : self.updated_at,
            'status'            : self.status.status,
            'service'           : self.service.service,
            'status_id'         : self.status_id,
            'account_id'        : self.account_id,
            'service_id'        : self.service_id,
            'meds'              : self.meds,
            'service_form'      : self.service.form
        }

class Inventory(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    item_code       = db.Column(db.String(100))
    item            = db.Column(db.String(100))
    min_quantity    = db.Column(db.Integer)
    max_quantity    = db.Column(db.Integer)
    reorder_level   = db.Column(db.Integer, default=10)
    
    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    items = db.relationship('Items',  backref='inventory', lazy=True)

    @hybrid_property
    def is_sufficient(self):
        return self.reorder_level < len([data for data in self.items if data.current_status == 5])

    @hybrid_property
    def all_items(self):
        return self.items
    
    @hybrid_property
    def available_items(self):
        return [data for data in self.items if data.current_status == 5]
    
    @hybrid_property
    def used_items(self):
        return [data for data in self.items if data.current_status == 6]
    
    @hybrid_property
    def expired_items(self):
        return [data for data in self.items if data.current_status == 7]

    # @hybrid_method
    # def get_item(self, id):
    #     return [data for data in self.items if data.id == id][0]
    
    def serialize(self):
        return {
            'id'                : self.id,
            'item_code'         : self.item_code,
            'item'              : self.item,
            'min_quantity'      : self.min_quantity,
            'max_quantity'      : self.max_quantity,
            'reorder_level'     : self.reorder_level
        }

class Items(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    expiry_date     = db.Column(db.DateTime)
    receive_date    = db.Column(db.DateTime)
    
    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    status_id       = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=True)
    inventory_id    = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=True)

    @hybrid_property
    def current_status(self):
        if self.expiry_date <= datetime.now() and self.status_id == 5:
            return 7
        else:
            return self.status_id

    def serialize(self):
        return {
            'id'            : self.id,
            'is_expired'    : self.expiry_date >= datetime.now(),
            'expiry_date'   : self.expiry_date.strftime('%m/%d/%Y') if self.expiry_date is not None else None,
            'receive_date'  : self.receive_date.strftime('%m/%d/%Y') if self.receive_date is not None else None,
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

    def serialize(self):
        return {
            'id'            : self.id,
            'role'          : self.role,
            'created_at'    : self.created_at,
            'updated_at'    : self.updated_at
        }
    
class Services(db.Model):

    id              = db.Column(db.Integer, primary_key=True)
    service         = db.Column(db.String(50))
    form            = db.Column(db.JSON)
    availability    = db.Column(db.Integer, default=3) # 1 for AM, 2 for PM, 3 for BOTH

    # timestamps
    created_at  = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # relationship
    appointment_service = db.relationship('Appointments',   backref='service', lazy=True)

    @hybrid_property
    def form_date(self):
        return json.loads(self.form)
    
    def serialize(self):
        return {
            'id'            : self.id,
            'service'       : self.service,
            'form'          : self.form,
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
    item_status         = db.relationship('Items',          backref='status', lazy=True)

    def serialize(self):
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

    def serialize(self):
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
