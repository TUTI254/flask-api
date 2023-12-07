import os 
from dotenv import load_dotenv
from flask import Flask, request, jsonify , make_response
from flask_sqlalchemy import SQLAlchemy


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
db = SQLAlchemy(app)

# create a table called users 
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True , nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'age': self.age, 'email': self.email}

with app.app_context():
    db.create_all()
    

@app.route('/', methods=['GET'])
def home():
    return "Welcome to my flask rest api project"

@app.route('/test', methods=['GET'])
def test():
    return make_response( jsonify({'message': 'This is a test route'}),200)



@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(name=data['name'], age=data['age'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'New user created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'Error creating user', 'error': str(e)}), 500)

@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return make_response(jsonify({'users': [user.json() for user in users]}), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting users', 'error': str(e)}), 500)

if __name__ == "__main__":
    app.run(debug=True)

# create a route called /users/<id> to get a specific user in the database
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first() # get the user with the specified id
        if user:
            return make_response(jsonify({'user': user.json()}), 200) # return a response to the user
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting user'}), 500)

# create a route called /users/<id> to update a specific user in the database
@app.route('/users/<int:id>', methods=['PATCH'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first() # get the user with the specified id
        if user:
            data = request.get_json() # get the data from the request
            user.name = data['name'] # update the name of the user
            user.age = data['age'] # update the age of the user
            user.email = data['email'] # update the email of the user
           
            db.session.commit() # commit the changes to the database
            return make_response(jsonify({'message': 'User updated'}), 200) # return a response to the user
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error updating user'}), 500)

# create a route called /users/<id> to delete a specific user in the database
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first() # get the user with the specified id
        if user:
            db.session.delete(user) # delete the user
            db.session.commit() # commit the changes to the database
            return make_response(jsonify({'message': 'User deleted'}), 200) # return a response to the user
        else:
            return make_response(jsonify({'message': 'User not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'Error deleting user'}), 500)
    
    

