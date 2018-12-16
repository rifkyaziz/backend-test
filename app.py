from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import config

app = Flask(__name__)
bcrypt = Bcrypt(app)
db_uri = 'mysql://{user}:{password}@{host}:{port}/{dbname}'.format(user = config.DATABASE_CONFIG['user'],
                                                                                    password = config.DATABASE_CONFIG['password'],
                                                                                    host = config.DATABASE_CONFIG['host'],
                                                                                    port = config.DATABASE_CONFIG['port'],
                                                                                    dbname = config.DATABASE_CONFIG['dbname'])
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'very-secure'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    products = db.relationship("Product")

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password
        }

# Product Model
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    size = db.Column(db.String(2))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, size, user_id):
        self.name = name
        self.size = size
        self.user_id = user_id
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def get_user(self):
        user = User.query.filter_by(id=self.user_id).first()
        return user.serialize()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "user": self.get_user()
        }

@app.route('/api/login', methods = ['POST'])
def login():
    req_data = request.get_json(force=True)
    if not req_data:
        return jsonify(message="Error, request data is not valid")

    access_token = create_access_token(identity=req_data["email"])
    return jsonify(access_token = access_token)

@app.route('/api/products', methods = ['POST'])
@jwt_required
def create_product():
    req_data = request.get_json(force=True)
    if not req_data:
        return jsonify(message="Error, request data is not valid")

    product = Product(req_data["name"],
                      req_data["size"],
                      req_data["user_id"])
    product.save()
    return jsonify(message="Successfully save data",
                   data=product.serialize())

@app.route('/api/products/<id>')
@jwt_required
def get_product(id):
    product = Product.query.filter_by(id=id).first()
    if not product:
        return jsonify(message="Product not found", data = {})
    
    return jsonify(message="Successfully get data",
                   data=product.serialize())

@app.route('/api/products/<id>', methods = ['PUT'])
@jwt_required
def update_product(id):
    req_data = request.get_json(force=True)
    if not req_data:
        return jsonify(message="Error, request data is not valid")
    
    product = Product.query.filter_by(id=id).first()
    if not product:
        return jsonify(message="Product not found", data = {})

    product.name = req_data["name"]
    product.size = req_data["size"]
    product.user_id = req_data["user_id"]
    db.session.commit()

    return jsonify(message="Successfully update data",
                   data=product.serialize())

@app.route('/api/products/<id>', methods = ['DELETE'])
@jwt_required
def delete_product(id):
    product = Product.query.filter_by(id=id).first()
    if not product:
        return jsonify(message="Product not found")
    
    db.session.delete(product)
    db.session.commit()
    return jsonify(message="Successfully delete data")

if __name__ == '__main__':
    app.run(debug=True)
