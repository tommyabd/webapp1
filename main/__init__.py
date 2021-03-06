import bcrypt
from flask import Flask
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import smtplib

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:\OSPanel\domains\GQSolar\main\static\img'
app.config['EXCEL_FOLDER'] = 'main\excel\BaseXlsx'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '5209a08cfb7acebb31ae9915' 
app.config['ALLOWED_IMAGE_EXTENSION'] = ['PNG','JPG', 'JPEG', 'GIF']
bcrypt  = Bcrypt(app)
db = SQLAlchemy(app)    
csrf = CSRFProtect(app)
migrate = Migrate(app,db)
ckeditor = CKEditor(app) 
loginmanager = LoginManager(app)

from main import routes


