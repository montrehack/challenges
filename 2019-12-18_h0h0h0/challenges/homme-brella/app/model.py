import datetime
from app import db

class msgdb(db.Model):
    # Data Model for mdown
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<text %r>' % self.text
