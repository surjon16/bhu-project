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
    
    case_number     = fields.Str(required=True)
    case_title      = fields.Str(required=True)
    location        = fields.Str(required=True)
    narrative       = fields.Str(required=True)
    date_reported   = fields.Str(required=True)
    date_record   = fields.Str(required=True)
    status_id       = fields.Str(required=True)
    patient     = fields.Str(required=True)
    respondent      = fields.Str(required=True)
    
    @validates('case_number')
    def validate_case_number(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a case number.')

    @validates('case_title')
    def validate_case_title(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a case title.')

    @validates('location')
    def validate_location(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a location.')

    @validates('narrative')
    def validate_narrative(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a narrative.')

    @validates('patient')
    def validate_patient(self, value):
        if value == '' or value is None:
            raise ValidationError('Please specify the patient.')

    @validates('respondent')
    def validate_respondent(self, value):
        if value == '' or value is None:
            raise ValidationError('Please specify the respondent.')

    @validates('status_id')
    def validate_status_id(self, value):
        if value == '' or value is None:
            raise ValidationError('Please specify the status.')

    @validates('date_reported')
    def validate_date_reported(self, value):
        if value == '' or value is None:
            raise ValidationError('Please specify the date reported.')

    @validates('date_record')
    def validate_date_record(self, value):
        if value == '' or value is None:
            raise ValidationError('Please specify the date of record.')


class CreateAppointmentSchema(Schema):
    
    details             = fields.Str(required=True)
    appointment            = fields.Str(required=True)
    record_id         = fields.Str(required=True)
    assigned_lupon_1    = fields.Str(required=True)
    
    @validates('details')
    def validate_details(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide details.')

    @validates('appointment')
    def validate_appointment(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide a appointment.')

    @validates('record_id')
    def validate_record_id(self, value):
        if value == '' or value is None:
            raise ValidationError('Please select a case to set appointment.')

    @validates('assigned_lupon_1')
    def validate_assigned_lupon_1(self, value):
        if value == '' or value is None:
            raise ValidationError('Please assign a lupon for this appointment.')

class CreateHearingSchema(Schema):

    minutes     = fields.Str(required=True)
    status_id   = fields.Str(required=True)

    @validates('minutes')
    def validate_minutes(self, value):
        if value == '' or value is None:
            raise ValidationError('Please provide the minutes of hearing.')

    @validates('status_id')
    def validate_status_id(self, value):
        if value == '' or value is None:
            raise ValidationError('Please specify the status of the case.')


 