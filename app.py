from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Enable CORS to allow requests from the frontend
CORS(app)

# Define a Volunteer model
class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

# Define a Food Donation model
class FoodDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    food_type = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    donation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Define a Cloth Donation model
class ClothDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    donationTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# Define a Money Donation model
class MoneyDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Float, nullable=False)

# Define an Other Donation model
class OtherDonation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    donationMessage = db.Column(db.String(500), nullable=False)
    donationTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Define a Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)

# Create the database and the tables
with app.app_context():
    db.create_all()

# Define the volunteer route
@app.route('/volunteer', methods=['POST'])
def volunteer():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        email = data.get('email')
        address = data.get('address')
        phone = data.get('phone')

        if not name or not email or not address or not phone:
            return jsonify({"error": "Missing required fields"}), 400

        new_volunteer = Volunteer(name=name, email=email, address=address, phone=phone)
        
        db.session.add(new_volunteer)
        db.session.commit()

        return jsonify({'message': 'Volunteer registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the food donation route
@app.route('/donation/food', methods=['POST'])
def food_donation():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        email = data.get('email')
        address = data.get('address')
        phone = data.get('phone')
        food_type = data.get('foodType')
        quantity = data.get('quantity')

        if not name or not email or not address or not phone or not food_type or not quantity:
            return jsonify({"error": "Missing required fields"}), 400

        new_food_donation = FoodDonation(name=name, email=email, address=address, phone=phone, food_type=food_type, quantity=quantity)
        
        db.session.add(new_food_donation)
        db.session.commit()

        return jsonify({'message': 'Food donation registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

# Define the cloth donation route
@app.route('/donation/cloth', methods=['POST'])
def cloth_donation():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Fetching the fields
        name = data.get('name')
        email = data.get('email')
        address = data.get('address')
        phone = data.get('phone')
        donationTime = data.get('donationTime')  # Corrected the key to match the frontend

        # Validate fields
        if not all([name, email, address, phone, donationTime]):
            return jsonify({"error": "Missing required fields"}), 400

        # Convert the donation_time to a datetime object
        try:
            donationTime = datetime.strptime(donationTime, "%Y-%m-%dT%H:%M")
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

        # Create a new ClothDonation entry
        new_cloth_donation = ClothDonation(
            name=name, 
            email=email, 
            address=address, 
            phone=phone, 
            donationTime=donationTime
        )
        
        db.session.add(new_cloth_donation)
        db.session.commit()

        return jsonify({'message': 'Cloth donation registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Define the money donation route
@app.route('/donation/money', methods=['POST'])
def money_donation():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        amount = data.get('amount')

        if not name or not email or not phone or not amount:
            return jsonify({"error": "Missing required fields"}), 400

        new_money_donation = MoneyDonation(name=name, email=email, phone=phone, amount=amount)
        
        db.session.add(new_money_donation)
        db.session.commit()

        return jsonify({'message': 'Money donation registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Define the other donation route
@app.route('/donation/other', methods=['POST'])
def other_donation():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        email = data.get('email')
        address = data.get('address')
        phone = data.get('phone')
        donationMessage = data.get('donationMessage')
        donationTime = data.get('donationTime')
        # Validate fields
        if not all([name, email, address, phone,donationMessage, donationTime]):
            return jsonify({"error": "Missing required fields"}), 400

        # Convert the donation_time to a datetime object
        try:
            donationTime = datetime.strptime(donationTime, "%Y-%m-%dT%H:%M")
        except ValueError:
            return jsonify({"error": "Invalid date format"}), 400

        # Create a new OtherDonation entry
        new_other_donation = OtherDonation(
            name=name, 
            email=email, 
            address=address, 
            phone=phone,
            donationMessage = donationMessage, 
            donationTime=donationTime
        )
        
        db.session.add(new_other_donation)
        db.session.commit()

        return jsonify({'message': 'other donation registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Define the contact route
@app.route('/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not name or not email or not message:
            return jsonify({"error": "Missing required fields"}), 400

        new_contact = Contact(name=name, email=email, message=message)
        
        db.session.add(new_contact)
        db.session.commit()

        return jsonify({'message': 'Contact submitted successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)