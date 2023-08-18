from flask import Flask, request, jsonify, make_response, Response
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps
import uuid
import jwt
import datetime
import secrets
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user-name:strong-password@localhost:5432/testdb"
app.config['SECRET_KEY'] = secrets.token_hex(16)
api = Api(app)
# api.namespaces[0].swagger = True
auth=api.namespace('', description='Authentication')
api.add_namespace(auth)
api.namespaces[0].authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-tokens'
    }
}

db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True)

class UserModel(db.Model):
    __tablename__ = 'user'
    
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)
    
    def __init__(self, name, email, password):
        # self.userId = userId
        self.name = name
        self.email = email
        self.password = password
    
    def to_dict(self):
        return {
            'userId': self.userId,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }



@auth.route("/signup", methods=["POST"])
class SignUp(Resource):
    @api.doc(responses={ 201: 'Created', 202: 'User already exists. Please Log in.' })
    @api.doc(parser = api.parser()
                .add_argument('name', type=str, required=True, help='Name', location='form')
                .add_argument('email', type=str, required=True, help='Email address', location='form')
                .add_argument('password', type=str, required=True, help='Password', location='form'))
    def post(self):
        data = request.form
        name, email, password = data['name'], data['email'], data['password']
        user = UserModel.query.filter_by(email=email).first()
        print(data, email, password, user)
        if user:
            return make_response('User already exists. Please Log in.', 202)
        user = UserModel(
            name = name, 
            email = email, 
            password = generate_password_hash(password, method='sha256')
            # password = password
        )
        db.session.add(user)
        db.session.commit()
        return make_response('Successfully registered.', 201)



@auth.route('/login', methods=['POST']) 
class LogIn(Resource):
    @api.doc(responses={ 200: 'Success', 401: 'Could not verify' })
    @api.doc(parser = api.parser()
            .add_argument('email', type=str, required=True, help='Email address', location='form')
            .add_argument('password', type=str, required=True, help='Password', location='form')
    )
    def post(self):
        auth = request.authorization
        data = request.form
        email, password = data['email'], data['password']  
        if auth:
            email, password = auth.email, auth.password
        if not email or not password: 
            return make_response('Could not verify', 401, {'Authentication': 'Credentials required"'})   
        
        user = UserModel.query.filter_by(email=email).first()  
        if not user: 
            return make_response('Could not verify', 401, {'Authentication': 'Invalid Email Address."'})   
        
        if check_password_hash(user.password, password):
            token = jwt.encode({
                        'userId' : user.userId, 
                        'email' : user.email, 
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
                    }, 
                    app.config['SECRET_KEY'], "HS256"
                )
            return jsonify({'token' : token})
        
        return make_response('Could not verify', 401, {'Authentication': 'Invalid Password."'}) 



def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       print(request.headers)
       if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
           print(token)
 
       if not token:
           return jsonify({'message': 'Token Missing!'}), 401
       try:
           data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
           user = UserModel.query.filter_by(email=data['email']).first()
       except jwt.ExpiredSignatureError:
           return jsonify({"message": "Token has expired"}), 401
       except jwt.InvalidTokenError:
           return jsonify({"message": "Invalid token"}), 401
       except:
           return jsonify({'message': 'Invalid Token. Please log in again.'}), 401
 
       return f(user, *args, **kwargs)
   return decorator



@auth.route("/hello", methods=["GET"])
# @api.doc(responses={ 200: 'Success', 401: 'Invalid Token. Please log in again.' })
# @api.doc(parser = api.parser().add_argument('x-access-tokens', type=str, required=True, help='Token', location='headers'))
class Home(Resource):
    @token_required
    def get(self):
        return [
            {
                'name' : user.name,
                'email' : user.email,
                'password' : user.password
            } for user in UserModel.query.all()
        ]
        
        
