from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False, default='')
    last_name = db.Column(db.String(150), nullable = False, default = '')
    email = db.Column(db.String(150), nullable = False)
    username = db.Column(db.String(25), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    token = db.Column(db.String, default = '', unique = True )
    g_auth_verify = db.Column(db.Boolean, default = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    # cars = db.relationship('Car', backref='user', lazy = True)

    def __init__(self, first_name='', last_name='', email='', username='' , password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.username = username
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash


    def __repr__(self):
        return f'User {self.email} has been added to the database.'


class Car(db.Model):
    # id = db.Column(db.String, primary_key = True)
    vin = db.Column(db.String(20), primary_key=True)
    make = db.Column(db.String(75), unique = False, nullable = False)
    model = db.Column(db.String(75), unique = False, nullable = False)
    year = db.Column(db.Integer,  unique = False, nullable = False)
    color = db.Column(db.String, unique = False, nullable = False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    
    
    def __init__(self,  vin, make, model, year, color,  user_token):
        # self.id = self.set_id()
        self.vin = vin
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.user_token = user_token
    
    
    def __repr__(self):
        return f'Car {self.year} {self.make} {self.model} has been added to the database'
    
 
class CarSchema(ma.Schema):
    class Meta:
        fields = ['vin', 'make', 'model', 'year', 'color', 'user_token']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)

