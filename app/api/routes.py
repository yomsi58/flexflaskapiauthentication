from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'Hello': 'All'}

@api.route('/cars', methods = ['POST'])
@token_required
def create(current_user_token):
    vin = request.json['vin']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token
    
    
    car = Car(vin, make, model,  year, color, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)



@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token, id):
    user_token = current_user_token.token
    car_Token = current_user_token.token
    if car_Token == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message': "Invalid Token"}), 401



@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, id):
    car_Token = current_user_token.token
    cars = Car.query.filter_by(user_token = car_Token).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update(current_user_token, id):
    car = Car.query.get(id) 
    vin = request.json['vin']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    user_token = current_user_token.token
    
    car.vin = vin
    car.make = make
    car.model = model
    car.year = year
    car.color = color
    car.user_token = current_user_token.token
    
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


    # user_token = current_user_token.token
    # car = Car.query.get(id)
    # if request.method == 'POST':
        
    #     if cars:
    #         db.session.delete(car)
    #         db.session.commit()
    #         return redirect(url_for('site.cars'))
    #     abort(404)
    
    
    # return redirect(url_for('site.cars'))



