from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '46af1a55a3a3992bdb12d4658e9a96e7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webapp.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
login_Manager = LoginManager(app)
login_Manager.login_view = 'login'
login_Manager.login_message_category = 'error'

from muya import routes