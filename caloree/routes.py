from flask import Flask, render_template, flash, redirect, url_for
from caloree.userdatabase import User, Food, Usercalorie
from caloree.forms import RegistrationForm, LoginForm
from caloree import app, db, bcrypt
from flask_login import login_user, logout_user

@app.route("/")                                                                                             
def index():                                                                                                
    return render_template('Index.html')

@app.route("/login", methods=['GET', 'POST'])                                                               
def login():                                                                                                
    form = LoginForm()                                                                                      
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful')
    return render_template('auth/login/login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])                                                            
def register():                                                                                             
    form = RegistrationForm()                                                                               
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))                                                                   
    return render_template('auth/register/register.html', form=form)

@app.route("/logout")                                                            
def register():
    logout_user()
    return redirect(url_for('index'))

