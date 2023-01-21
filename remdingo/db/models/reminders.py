from sqlalchemy import Index

from remdingo.app import db


class Reminders(db.Model):
    __tablename__ = "reminders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50))
    reminder_date_utc = db.Column(db.DateTime)
    reminder_date_user = db.Column(db.DateTime)
    reminder_text = db.Column(db.String(500))
    snooze_number = db.Column(db.Integer, default=0)
    ack = db.Column(db.Boolean, default=False)
    sms = db.Column(db.Boolean, default=False)
    email = db.Column(db.Boolean, default=False)
    web = db.Column(db.Boolean, default=True)
    offset = db.Column(db.Integer, default=0)
    tz = db.Column(db.String(300))
    created = db.Column(db.DateTime)

    Index('reminders_idx', customer_id, reminder_date_utc)
