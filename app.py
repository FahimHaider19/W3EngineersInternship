from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user-name:strong-password@localhost:5432/testdb"
db = SQLAlchemy(app)

class UserModel(db.Model):
    __tablename__ = 'user'
    
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    password = db.Column(db.String(50), nullable=True)
    
    def __init__(self, userId, name, email, password):
        self.userId = userId
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

@app.route("/")
def home():
    return [
        {
            "userId": user.userId,
            "name": user.name,
            "email": user.email,
            "password": user.password
        } for user in UserModel.query.all()
    ]

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email, password = data.get('email'), data.get('password')
    user = UserModel.query.filter_by(email=email).first()
    if user:
        return "Email already exists"
    user = UserModel(None, data.get('name'), email, password)
    db.session.add(user)
    db.session.commit()
    return user.to_dict()