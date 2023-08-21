from flask import Flask, request, jsonify, make_response, Response
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import UserModel
from app import db
from app import swagger

auth = Namespace('Auth', description='Authentication')
auth.authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'authorization'
    }
}
auth.security='apikey' 


@auth.route("/signup", methods=["POST"])
class SignUp(Resource):
    @auth.doc(responses={ 201: 'Created', 202: 'User already exists. Please Log in.' })
    @auth.doc(parser = auth.parser()
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
    @auth.doc(responses={ 200: 'Success', 401: 'Could not verify' })
    @auth.doc(parser = auth.parser()
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
            access_token = create_access_token(identity=email)
            return {'access_token': 'Bearer ' + access_token}, 200
        
        return make_response('Could not verify', 401, {'Authentication': 'Invalid Password."'}) 



@auth.route("/users", methods=["GET"])
class Home(Resource):
    @auth.doc(security='apikey')
    @jwt_required()
    def get(self):
        return [
            {
                'name' : user.name,
                'email' : user.email,
                'password' : user.password
            } for user in UserModel.query.all()
        ]



snf = Namespace('', description='Search and Filter')


@snf.route("/search", methods=["GET"])
class Search(Resource):
    @snf.doc(responses={ 200: 'Success', 401: 'Could not verify' })
    @snf.doc(parser = snf.parser()
            .add_argument('title', type=str, required=True, help='Title', location='form')
            .add_argument('minprice', type=str, required=True, help='Min Price', location='form')
            .add_argument('maxprice', type=str, required=True, help='Max Price', location='form')
            .add_argument('location', type=str, required=True, help='Location', location='form')
            .add_argument('amenities', type=str, required=True, help='Ameities', location='form')
    )
    def get(self):
        data = request.form
        search = data['search']
        return make_response(search, 200)


@snf.route("/filter", methods=["GET"])
class Filter(Resource):
    @snf.doc(responses={ 200: 'Success', 401: 'Could not verify' })
    @snf.doc(parser = snf.parser()
            .add_argument('filter', type=str, required=True, help='Filter', location='form')
    )
    def get(self):
        data = request.form
        filter = data['filter']
        return make_response(filter, 200)