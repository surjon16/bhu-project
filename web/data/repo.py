from data.repositories.accounts         import AccountsRepo
from data.repositories.appointments     import AppointmentsRepo
from data.repositories.inventory        import InventoryRepo
from data.repositories.items            import ItemsRepo
from data.repositories.notifications    import NotificationsRepo
from data.repositories.records          import RecordsRepo
from data.repositories.roles            import RolesRepo
from data.repositories.services         import ServicesRepo
from data.repositories.status           import StatusRepo

class Repository(AccountsRepo, AppointmentsRepo, InventoryRepo, ItemsRepo, NotificationsRepo, RecordsRepo, RolesRepo, ServicesRepo, StatusRepo):

    def __init__(self):
        pass

# =============================================================================================

    # def populate():

    #     # create roles

    #     role = Roles(role='admin')
    #     db.session.add(role)

    #     role = Roles(role='staff')
    #     db.session.add(role)

    #     role = Roles(role='patient')
    #     db.session.add(role)

    #     # create status

    #     status = Status(status='Approved')
    #     db.session.add(status)

    #     status = Status(status='Declined')
    #     db.session.add(status)

    #     status = Status(status='Cancelled')
    #     db.session.add(status)

    #     status = Status(status='Pending')
    #     db.session.add(status)

    #     status = Status(status='Available')
    #     db.session.add(status)

    #     status = Status(status='Used')
    #     db.session.add(status)

    #     status = Status(status='Expired')
    #     db.session.add(status)

    #     # create accounts

    #     account = Accounts(
    #         first_name  = 'System',
    #         middle_name = '',
    #         last_name   = 'Administrator',
    #         gender      = '',
    #         civil       = '',
    #         phone       = '+639354796747',
    #         birth_date  = '',
    #         address     = 'CDO',
    #         email       = 'admin@gmail.com',
    #         password    = 'admin1234',
    #         occupation    = 'Barangay Health Worker',
    #         role_id     = 1
    #     )
    #     db.session.add(account)

    #     account = Accounts(
    #         first_name  = 'Sample',
    #         middle_name = '',
    #         last_name   = 'Patient',
    #         gender      = '',
    #         civil       = '',
    #         phone       = '+639354796747',
    #         birth_date  = '',
    #         address     = 'CDO',
    #         email       = 'patient@gmail.com',
    #         password    = 'admin1234',
    #         occupation    = '',
    #         role_id     = 3
    #     )
    #     db.session.add(account)

    #     # create service

    #     service = Services(
    #         service  = 'Immunize'
    #     )
    #     db.session.add(service)

    #     db.session.commit()

    #     return True    