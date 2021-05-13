from application import app
from data import db

app.secret_key = 'bhu_management_system'

if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    app.run(debug=True, host='192.168.110.102', port='8080')
