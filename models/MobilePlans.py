from db import db

class MobilePlans(db.Model):
    __tablename__ = 'mobileplans'
    PlanID  = db.Column(db.Integer, primary_key=True)
    PlanName = db.Column(db.String(50), nullable=False, primary_key=False)
    MonthlyAllowanceData  = db.Column(db.Integer)
    MonthlyAllowanceTalkTime  = db.Column(db.Integer)
    MonthlyAllowanceTextMessages  = db.Column(db.Integer)