from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from models import db, User, Car, car_schema, cars_schema
from flask_login import current_user, login_required


site = Blueprint('site', __name__,template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@site.route('/cars')
@login_required
def cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)

@site.route('/create_car', methods=['POST'])
@login_required
def create_car():
    vin = request.form['vin']
    year = request.form['year']
    make = request.form['make']
    model = request.form['model']
    color = request.form['color']
    user_token = current_user.token
    
    car = Car(vin=vin, year=year, make=make, model=model, color=color, user_token = user_token )
    db.session.add(car)
    db.session.commit()
    
    return redirect(url_for('site.cars'))


@site.route('/update_car/<string:vin>', methods=['POST', 'GET'])
@login_required
def update_car(vin):
    car = Car.query.get(vin)
    car = Car.query.filter_by(vin=vin).first()
    if request.method == 'POST':
        # db.session.delete(car)
        # db.session.commit()
        if car:
    
            vin = request.form['vin']
            year = request.form['year']
            make = request.form['make']
            model = request.form['model']
            color = request.form['color']
            user_token = current_user.token
            
            car = Car( vin = vin, year = year, make = make, model = model, color = color, user_token = user_token)

    
            db.session.add(car)
            db.session.commit()
            return  redirect(url_for('site.cars'))
        return f"Vin {vin} is not valid."
    return render_template('update.html', car=car)
        
    
    # return redirect(url_for('site.cars'))
    

@site.route('/delete_car/<id>', methods=['POST', 'GET', 'PUT'])
@login_required
def delete_car(id):
    car = Car.query.get(id)
    if request.method == 'POST':
        
        if cars:
            db.session.delete(car)
            db.session.commit()
            return redirect(url_for('site.cars'))
        abort(404)
    
    
    return redirect(url_for('site.cars'))

