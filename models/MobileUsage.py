from db import db

class MobileUsage(db.Model):
    __tablename__ = 'mobileusage'
    UsageID  = db.Column(db.Integer, primary_key=True)
    DataUsage  = db.Column(db.Integer)
    CallsUsage  = db.Column(db.Integer)
    TextUsage  = db.Column(db.Integer)
    InternationalRoaming  = db.Column(db.Boolean, default=False)
    MobileNumberID  = db.Column(db.Integer, db.ForeignKey('mobilenumbers.MobileNumberID'), nullable=False)
