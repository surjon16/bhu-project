from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from application import app

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/db_bhu' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://Roannie:admin1234@Roannie.mysql.pythonanywhere-services.com/Roannie$db_bhu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

csrf = CSRFProtect()
csrf.init_app(app)