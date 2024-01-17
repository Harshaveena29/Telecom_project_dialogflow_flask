from db import db

class Customers(db.Model):
    __tablename__ = 'customers'
    CustomerID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    mobile_numbers = db.relationship('MobileNumbers', backref='customer', lazy=True)