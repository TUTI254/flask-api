import os 
from dotenv import load_dotenv
from flask import Flask
from model.users.models import db
from controller.users.controllers import user_controller

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')

db.init_app(app)

app.register_blueprint(user_controller)

with app.app_context():
    db.create_all()

