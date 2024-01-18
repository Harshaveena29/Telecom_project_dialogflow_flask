import os
from flask import Flask
from db import db
from routes import webhook 
from dotenv import load_dotenv

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv("DATABASE_URL") 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database
    db.init_app(app)

    # Register your routes
    app.register_blueprint(webhook)

    return(app)
