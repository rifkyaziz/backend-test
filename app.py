from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.bcrypt import Bcrypt

import config

app = Flask(__name__)
bcrypt = Bcrypt(app)
db_uri = 'mysql://{user}:{password}@{host}:{port}/{dbname}?useSSL=false'.format(user = config.DATABASE_CONFIG['user'],
                                                                                    password = config.DATABASE_CONFIG['password'],
                                                                                    host = config.DATABASE_CONFIG['host'],
                                                                                    port = config.DATABASE_CONFIG['port'],
                                                                                    dbname = config.DATABASE_CONFIG['dbname'])
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    products = relationship("Product")

    def __init__(self, email, password, products):
        self.email = email
        self.password = bcrypt(password)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    size = db.Column(db.String(2))
    user_id = Column(db.Integer, db.ForeignKey('users.id'))

@app.route('/products')
def get_all_products():
    return "Hello, World"

if __name__ == '__main__':
    app.run(debug=True)
    
