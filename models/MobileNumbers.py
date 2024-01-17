from db import db

class MobileNumbers(db.Model):
    __tablename__ = 'mobilenumbers'
    MobileNumberID = db.Column(db.Integer, primary_key=True)
    MobileNumber = db.Column(db.String(20), unique=True, nullable=False)
    CustomerID = db.Column(db.Integer, db.ForeignKey('customers.CustomerID'), nullable=False)
    PlanID = db.Column(db.Integer, db.ForeignKey('mobileplans.PlanID'), nullable=False)
    IsActive = db.Column(db.Boolean, nullable=False)
    mobile_plan = db.relationship('MobilePlans', backref='mobile_number', lazy=True)
    mobile_usage = db.relationship('MobileUsage', backref='mobile_number', lazy=True)