from flask import Flask, render_template, flash, redirect, url_for, request
from caloree.userdatabase import User, Food, Usercalorie
from caloree.forms import RegistrationForm, LoginForm, PictureForm
from caloree import app, db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
from werkzeug import SharedDataMiddleware
from caloree.predict import predict

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            predicted_food = predict('caloree/static/uploads/' + filename)
            name = Food.query.filter_by(name=predicted_food).first().name
            name = name.replace("_", " ")
            name = name.title()
            calorie = Food.query.filter_by(name=predicted_food).first().calorie
            carbs = Food.query.filter_by(name=predicted_food).first().carbs
            fibre = Food.query.filter_by(name=predicted_food).first().fibre
            fats = Food.query.filter_by(name=predicted_food).first().fats
            protein = Food.query.filter_by(name=predicted_food).first().protein
            return render_template('prediction.html', name=name, calorie=calorie, carbs=carbs, fibre=fibre, fats=fats, protein=protein, filename=filename)
    if current_user.is_authenticated:
        return redirect(url_for('loggedin'))
    else:
        return render_template('Index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/login", methods=['GET', 'POST'])                                                               
def login():                                                                                                
    form = LoginForm()                                                                                      
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('upload_file'))
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
def logout():
    logout_user()
    return redirect(url_for('upload_file'))

@app.route("/refresh")
def refresh():
    current_user.calories = 2200
    db.session.commit()
    return redirect(url_for('upload_file'))

@app.route("/loggedin", methods=['GET', 'POST'])
@login_required
def loggedin():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            predicted_food = predict('caloree/static/uploads/' + filename)
            name = Food.query.filter_by(name=predicted_food).first().name
            name = name.replace("_", " ")
            name = name.title()
            user = current_user.username
            usercal = current_user.calories
            calorie = Food.query.filter_by(name=predicted_food).first().calorie
            current_user.calories -= calorie
            usercal = usercal - calorie
            db.session.commit()
            carbs = Food.query.filter_by(name=predicted_food).first().carbs
            fibre = Food.query.filter_by(name=predicted_food).first().fibre
            fats = Food.query.filter_by(name=predicted_food).first().fats
            protein = Food.query.filter_by(name=predicted_food).first().protein
            return render_template('PredictionWithCalLeft.html', name=name, calorie=calorie, carbs=carbs, fibre=fibre, fats=fats, protein=protein, filename=filename, user=user, usercal=usercal)
    user = current_user.username
    usercal = current_user.calories
    return render_template('IndexWithCalLeft.html', user=user, usercal=usercal)
