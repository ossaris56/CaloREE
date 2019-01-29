from flask import Flask, render_template, flash, redirect, url_for, request
from caloree.userdatabase import User, Food, Usercalorie
from caloree.forms import RegistrationForm, LoginForm, PictureForm
from caloree import app, db, bcrypt
from flask_login import login_user, logout_user
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
            print('hi')
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
            predict('caloree/uploads/' + filename)
            os.system("rm -r ~/CaloREE/caloree/uploads/*.jpg")
                
    return render_template('Index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

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
def logout():
    logout_user()
    return redirect(url_for('index'))


