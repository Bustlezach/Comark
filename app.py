from flask import (
    Flask, render_template, jsonify, request, flash, redirect, url_for
)
from user import user
# from geopy.geocoders import Nominatim
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user
)
from flask_bcrypt import Bcrypt
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comark.db"
app.config["SECRET_KEY"] = "random string"
db = SQLAlchemy()
login_manager = LoginManager(app)
login_manager.init_app(app)
app.register_blueprint(user, url_prefix="/user")
bcrypt = Bcrypt(app)



class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.Text, nullable=False)
    location = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    country = db.Column(db.String)

    def __repr__(self):
        return f"Username: {self.username}, Name: {self.name}, Phone Number: {self.phone_number}"


class Product(db.Model, UserMixin):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_link = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    def __repr__(self):
        return f"The product name is {self.product_name}, and it costs {self.price}."


db.init_app(app)
with app.app_context():
    db.create_all()


# creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


# def get_coords():
#     client = Nominatim(user_agent="my_app")
#     location = client.geocode("My current location")
#     lat = location.latitude
#     long = location.longitude
#     return lat, long  # Return both latitude and longitude


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        phone_number = request.form['phone_number']
        address = request.form['home_address']
        location = request.form['location']
        state = request.form['state']
        country = request.form['country']

        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        
        user = User(
            username=username, password=password, name=name, 
            phone_number=phone_number, address=address, location=location, 
            state=state, country=country
            )
        
        db.session.add(user)
        db.session.commit()
        flash(f"{username}, you have been registered!")
        return redirect(url_for('index'))
    return render_template('sign_up.html')




# @app.route('/login', methods=['POST'])
# def login():
#     if request.method == 'POST':
#         if not request.form['username'] \
#             or not requests.form['password']:
#             flash("Please, enter the fields.", "error")


# @app.route('/receive_coordinates', methods=['POST'])
# def receive_coordinates():
#     if request.method == 'POST':
#         res = request.get_json()
#         lat = res.get('latitude')
#         long = res.get('longitude')
#         KEY = '7CjHpcOpgKkcKI73yNKxUSyGZdzJKmZn'
#         url = f'https://www.mapquestapi.com/geocoding/v1/reverse?key={KEY}&location={lat},{long}&includeRoadMetadata=true&includeNearestIntersection=true'
#         message = requests.get(url)
#         if (message.status_code is 200):
#             res = message.json()
#             results = res.get('results')
#             city = results[0]['locations'][0]['adminArea5']
#             return city



if __name__ == '__main__':
    app.run(debug=True)
