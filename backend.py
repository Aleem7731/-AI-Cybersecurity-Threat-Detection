from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
CORS(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# API Route: User Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except:
        return jsonify({"error": "Username already exists"}), 400

# API Route: User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        session['user'] = user.username
        return jsonify({"message": "Login successful", "username": user.username}), 200
    return jsonify({"error": "Invalid username or password"}), 401

# API Route: Phishing Detection (Dummy Logic)
@app.route('/predict/email', methods=['POST'])
def predict_email():
    data = request.json
    email_text = data.get('email_text', "")
    prediction = "Phishing" if "urgent" in email_text.lower() else "Safe"
    return jsonify({"prediction": prediction})

@app.route('/predict/url', methods=['POST'])
def predict_url():
    data = request.json
    url = data.get('url', "")
    prediction = "Phishing" if "suspicious" in url.lower() else "Safe"
    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
