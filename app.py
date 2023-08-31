from flask import (
    Flask, render_template, request, flash, redirect, url_for
)

from geopy.geocoders import Nominatim
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
bcrypt = Bcrypt(app)


class User(db.Model, UserMixin):
    """
    This class provides data for the users
    table in the database
    """
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    country = db.Column(db.String)

    products = db.relationship('Product', backref='users ')

    def get_id(self):
        return str(self.user_id)  # Convert to string as required

    def __repr__(self):
        return f"Username: {self.username}, Name: {self.name}, Phone Number: {self.phone_number}"


class Product(db.Model, UserMixin):
    """
    This class provides data for the products
    table in the database
    """
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key = True)
    product_name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_link = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    username = db.Column(db.Integer, db.ForeignKey("users.username"))


    def get_id(self):
        return str(self.product_id_id)  # Convert to string as required

    def __repr__(self):
        return f"The product name is {self.product_name}, and it costs {self.price}."


"""Initialise the database"""
db.init_app(app)
with app.app_context():
    db.create_all()


# creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return User.query.get(user_id)


def get_coords():
    client = Nominatim(user_agent="my_app")
    location = client.geocode("My current location")
    lat = location.latitude
    long = location.longitude
#    return lat, long  # Return both latitude and longitude
    KEY = '7CjHpcOpgKkcKI73yNKxUSyGZdzJKmZn'
    url = f'https://www.mapquestapi.com/geocoding/v1/reverse?key={KEY}&location={lat},{long}&includeRoadMetadata=true&includeNearestIntersection=true'
    message = requests.get(url)
    if (message.status_code == 200):
        res = message.json()
        results = res.get('results')
        city = results[0]['locations'][0]['adminArea5']
        return city



@app.route('/')
def index():
    """The landing page route"""
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/about')
def about():
    """The about page route"""
    return render_template('about.html')


@app.route('/team')
def team():
    """The team page route"""
    return render_template('team.html')


@app.route('/sign_up')
def sign_up():
    """The sign up page route."""
    return render_template('sign_up.html')


@app.route('/register_user', methods=['POST'])
def register_user():
    """
    The form filled in the sign up page is submitted
    to register route where it is processed and
    stored in the database on success and redirected to
    sign up page on failure.
    """
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        phone_number = request.form['phone_number']
        address = request.form['address']
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


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        if not request.form['username'] or \
                not request.form['password']:
            flash("Fill in your username and password to login.")
        else:
            user = User.query.filter_by(username=request.form['username']).first()
            if user and \
                    bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                flash(f"Welcome, {user.name}!")
                return redirect(url_for('user_page', user_id=user.user_id))  # Use user.user_id
            else:
                flash('Invalid username or password')
    return redirect(url_for('index'))



@login_required
@app.route('/user/<user_id>')
def user_page(user_id):
    posts = Product.query.filter_by(user_id=user_id).all()
    return render_template('user.html', title='User Homepage', posts=posts)


@login_required
@app.route('/user/addPost', methods=['POST'])
def add_post():
    if request.method == 'POST':
        product_name = request.form['product_name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']
        img_link = request.form['image_link']
        product = Product(
            product_name=product_name, category=category, price=price,
            description=description, img_link=img_link
            )
        
        db.session.add(product)
        db.session.commit()
        flash(f"{product_name} is posted successfully.")
        return redirect(url_for('user_page'))
    return render_template('add_post.html', title='Create Product')


@login_required
@app.route('/user/update<int:product_id>', methods=['POST', 'GET'])
def update(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if request.method == 'POST':
        new_product_name = request.form['product_name']
        new_category = request.form['category']
        new_price = request.form['price']
        new_description = request.form['description']
        new_img_link = request.form['image_link']
        product.product_name = new_product_name
        product.category = new_category
        product.price = new_price
        product.description = new_description
        product.img_link = new_img_link

        db.session.commit()
        flash(f"{new_product_name} has been updated successfully.")
        return redirect(url_for('user_page'))



@login_required
@app.route('/user/delete/<product_id>')
def delete(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.")
    return redirect(url_for('user_page'))


@login_required
@app.route('/user/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)