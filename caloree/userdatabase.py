from caloree import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
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
        return f"name('{self.name}', '{self.calorie}', '{self.carbs}', '{self.fibre}', '{self.fats}', '{self.protein}')"

class Usercalorie(db.Model):                                                                                
    id = db.Column(db.Integer, primary_key=True)                                                            
    name = db.Column(db.String(30), unique=True, nullable=False)                                            
    calorie = db.Column(db.Integer , nullable=False)                                                        
    carbs = db.Column(db.Integer , nullable=False)                                                          
    fibre = db.Column(db.Integer , nullable=False)                                                          
    fats = db.Column(db.Integer , nullable=False)                                                           
    protein = db.Column(db.Integer , nullable=False)
    user_image = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"name('{self.name}', '{self.calorie}', '{self.carbs}', '{self.fibre}', '{self.fats}', '{self.protein}', '{self.user_id}')"
