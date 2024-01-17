import os
from flask import Flask
from db import db
from routes import webhook  # Import the 'webhook' route from the 'routes' module

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)



# Register your routes
app.register_blueprint(webhook)

if __name__ == '__main__':
    app.run()
