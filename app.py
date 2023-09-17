from flask import (
    Flask, render_template, request, flash, redirect, url_for
)
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, login_required, logout_user, current_user
)
from flask_bcrypt import Bcrypt
import requests, uuid, os


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

    products = db.relationship(
        'Product', backref='user', lazy='dynamic', foreign_keys='Product.user_id'
    )

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
    product_id = db.Column(db.String, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255))
    price = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_link = db.Column(db.String)
    user_id = db.Column(db.String(255), db.ForeignKey("users.user_id"), primary_key=True)
    username = db.Column(db.String(255), db.ForeignKey("users.username"))


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


"""Alternative for GEOLOCATION API"""
"""
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
"""

@app.route('/')
def index():
    """The landing page route"""
    title = 'Homepage'
    products = Product.query.order_by(Product.product_id.desc()).all()
    return render_template('index.html', products=products, title=title,
                           cache_id=uuid.uuid4().__str__())



@app.route('/search', methods=['POST'])
def search():
    """Make a request to the ipinfo.io API"""
    response = requests.get("https://ipinfo.io/json")
    ip_address = response.json()["ip"]
    response_ip = requests.get(f"https://ipinfo.io/{ip_address}/json")
    data_ip = response_ip.json()

    # Extract the latitude and longitude
    latitude, longitude = data_ip["loc"].split(",")

    # Print the latitude and longitude
    print(f"Latitude: {latitude}, Longitude: {longitude}")

    """Make a request to the ipgeolocation.abstractapi.com API"""

    url = "https://ipgeolocation.abstractapi.com/v1/?api_key=9fabc1053c684dc49448caeb978652ab"
    resp = requests.request("GET", url)
    data_json = resp.json()
    city = data_json.get('city')

    searched_product = request.form['search_item']
    if not searched_product:
            flash("Please provide a search term")
            return redirect(url_for('index'))

    # products = Product.query.filter(Product.product_name.ilike(f'%{searched_product}%')).all()
    # return render_template('index.html', products=products, title='Search')

    if not city:
        products = Product.query.filter(Product.product_name.ilike(f'%{searched_product}%')).all()
        return render_template('index.html', products=products, title='Homepage')
    else:
        products = Product.query.filter(
            or_(
                Product.product_name.ilike(f'%{searched_product}%'),
                User.location.ilike(f'%{city}%')
            )
        ).all()
        return render_template('index.html', products=products, title='Search')


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



@app.route('/register_user', methods=['POST', 'GET'])
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
    return render_template('sign_up.html', title = 'Sign up')


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
    return render_template('user.html', title='User-Homepage', posts=posts)


@login_required
@app.route('/user/create')
def create():
    user_id = current_user.get_id()
    return render_template('create_product.html', user_id=user_id)



@login_required
@app.route('/user/add_post/<user_id>', methods=['POST'])
def add_post(user_id):
    """Add product to the database."""
    user = User.query.filter_by(user_id=user_id).first()
    username = user.username

    if request.method == 'POST':
        product_id = str(uuid.uuid4())
        product_name = request.form['product_name']
        category = request.form['category']
        price = request.form['price']
        description = request.form['description']
        img_link = request.form['image_link']

        if not product_name or not category \
        or not price or not description or not img_link:
            flash("Please, fill all fields.")
            return render_template('create_product.html', title='Create Product')

        product = Product(
            product_id=product_id,
            product_name=product_name, category=category, price=price,
            description=description, img_link=img_link, user_id=user_id,
            username=username
            )

        db.session.add(product)
        db.session.commit()
        flash(f"{product_name} is posted successfully.")
        return redirect(url_for('user_page', user_id=user_id))


@login_required
@app.route('/user/update/<string:product_id>', methods=['POST'])
def update(product_id):
    user_id = current_user.get_id()
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
        return redirect(url_for('user_page', user_id=user_id))
    else:
        pass


@login_required
@app.route('/user/linkupdate/<string:product_id>')
def link_update(product_id):
    post = Product.query.filter_by(product_id=product_id).first()
    return render_template('update.html', product_id=product_id, post=post)



@login_required
@app.route('/user/delete/<product_id>')
def delete(product_id):
    user_id = current_user.get_id()
    product = Product.query.filter_by(product_id=product_id).first()
    if product is not None:
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted.")
    return redirect(url_for('user_page',  user_id=user_id))


@login_required
@app.route('/user/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    # port = int(os.environ.get('PORT', 5000))
    # app.run(host='0.0.0.0', port=port)