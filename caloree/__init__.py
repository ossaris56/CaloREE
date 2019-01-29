from flask import Flask, render_template, flash, redirect, url_for                                          
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)                                                                                       
app.config['SECRET_KEY'] = 'dev'                                                                            
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'                                                  
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from caloree import routes
