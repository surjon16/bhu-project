from datetime import datetime
from marshmallow import Schema, fields, validates, ValidationError

# All classes declared will be used for validation

class CreateAccountSchema(Schema):
    
    first_name  = fields.Str(required=True)
    last_name   = fields.Str(required=True)
    phone       = fields.Str(required=True)
    email       = fields.Email(required=True)
    address     = fields.Str(required=True)
    password    = fields.Str(required=True)

    @validates('first_name')
    def validate_first_name(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide your first name.')

    @validates('last_name')
    def validate_last_name(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide your last name.')

    @validates('phone')
    def validate_phone(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a phone number.')
        if value[:4] != '+639':
            raise ValidationError('Invalid phone number.')
        if len(value) != 13:
            raise ValidationError('Invalid phone number.')

    @validates('address')
    def validate_address(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide an address.')

    @validates('password')
    def validate_password(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a password.')

class UpdateAccountSchema(Schema):
    
    first_name  = fields.Str(required=True)
    last_name   = fields.Str(required=True)
    phone       = fields.Str(required=True)
    email       = fields.Email(required=True)
    address     = fields.Str(required=True)
    role_id     = fields.Str(required=True)

    @validates('first_name')
    def validate_first_name(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide your first name.')

    @validates('last_name')
    def validate_last_name(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide your last name.')

    @validates('phone')
    def validate_phone(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a phone number.')
        if value[:4] != '+639':
            raise ValidationError('Invalid phone number.')
        if len(value) != 13:
            raise ValidationError('Invalid phone number.')

    @validates('address')
    def validate_address(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide an address.')

    @validates('role_id')
    def validate_role_id(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a role.')


class RegisterAccountSchema(Schema):

    first_name  = fields.Str(required=True)
    last_name   = fields.Str(required=True)
    email       = fields.Email(required=True)
    phone       = fields.Str(required=True)
    password    = fields.Str(required=True)

    @validates('first_name')
    def validate_first_name(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide your first name.')

    @validates('last_name')
    def validate_last_name(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide your last name.')

    @validates('phone')
    def validate_phone(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a phone number.')
        if value[:4] != '+639':
            raise ValidationError('Invalid phone number.')
        if len(value) < 13 :
            raise ValidationError('Invalid phone number.')

    @validates('password')
    def validate_password(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a password.')


class CreateRecordSchema(Schema):
    
    record_number   = fields.Str(required=True)
    record_details  = fields.Str(required=True)
    record_date   = fields.Str(required=True)
    
    @validates('record_number')
    def validate_record_number(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a record number.')

    @validates('record_details')
    def validate_record_details(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide the details.')

    @validates('record_date')
    def validate_record_date(self, value):
        if value == '' or value is None:
            raise ValidationError('Please specify the date.')


class CreateAppointmentSchema(Schema):
    
    details             = fields.Str(required=True)
    appointment_date    = fields.Str(required=True)
    account_id          = fields.Str(required=True)
    status_id           = fields.Str(required=True)
    service_id          = fields.Str(required=True)
    
    @validates('details')
    def validate_details(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide details.')

    @validates('appointment_date')
    def validate_appointment_date(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide an appointment.')

    @validates('account_id')
    def validate_account_id(self, value):
        if value == '' or value is None:
            raise ValidationError('Please select an account for this appointment.')

    @validates('status_id')
    def validate_status_id(self, value):
        if value == '' or value is None:
            raise ValidationError('Please select a status.')

    @validates('service_id')
    def validate_service_id(self, value):
        if value == '' or value is None:
            raise ValidationError('Please select a service.')

class CreateServiceSchema(Schema):

    service         = fields.Str(required=True)
    availability    = fields.Str(required=True)

    @validates('service')
    def validate_service(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a service name.')

    # @validates('availability')
    # def validate_availability(self, value):
    #     if value == '' or value is None:
    #         raise ValidationError('Please specify the availability.')


class CreateInventorySchema(Schema):

    item            = fields.Str(required=True)
    quantity        = fields.Str(required=True)
    # expiry_date     = fields.Str(required=True)

    @validates('item')
    def validate_item(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide an item name.')

    @validates('quantity')
    def validate_quantity(self, value):
        if value == '' or value is None:
            raise ValidationError('Please indicate the quantity.')

    # @validates('expiry_date')
    # def validate_expiry_date(self, value):
    #     if value == '' or value is None:
    #         raise ValidationError('Please specify the expiry date.')
