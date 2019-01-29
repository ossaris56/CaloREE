from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    calories = db.Column(db.Integer, nullable=False, default=2200)
    eaten = db.relationship('Usercalorie', backref='consumed', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.calories}')"

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    calorie = db.Column(db.Integer , nullable=False)
    carbs = db.Column(db.Integer , nullable=False)
    fibre = db.Column(db.Integer , nullable=False)
    fats = db.Column(db.Integer , nullable=False)
    protein = db.Column(db.Integer , nullable=False)

    def __repr__(self):
        return f"name('{self.name}', '{self.calorie}', '{self.calorie}', '{self.calorie}', '{self.calorie}', '{self.calorie}')"

class Usercalorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    calorie = db.Column(db.Integer , nullable=False)
    carbs = db.Column(db.Integer , nullable=False)
    fibre = db.Column(db.Integer , nullable=False)
    fats = db.Column(db.Integer , nullable=False)
    protein = db.Column(db.Integer , nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"name('{self.name}', '{self.calorie}', '{self.calorie}', '{self.calorie}', '{self.calorie}', '{self.calorie}')"

@app.route("/")
def index():
    return render_template('Index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('auth/login/login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('auth/register/register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True, port=8234,ssl_context='adhoc', host="0.0.0.0")
