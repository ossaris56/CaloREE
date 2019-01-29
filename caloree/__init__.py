from flask import Flask, render_template, flash, redirect, url_for                                          
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
UPLOAD_FOLDER = 'caloree/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['SECRET_KEY'] = 'dev'                                                                            
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from caloree import routes
