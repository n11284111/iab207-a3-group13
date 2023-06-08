from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    emailid = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(20))
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    events = db.relationship('Event', backref='user')
    bookings = db.relationship('Booking', backref='user')

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now)
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
    
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    artist = db.Column(db.String(30))
    description = db.Column(db.String(200))
    genre = db.Column(db.String(20))
    location = db.Column(db.String(100))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    tickets = db.Column(db.Integer)
    ticket_price = db.Column(db.Float)    
    image = db.Column(db.String(400))
    status = db.Column(db.String(20), default="Open")
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # ... Create the Comments db.relationship
	# relation to call events.comments and comment.event
    comments = db.relationship('Comment', backref='event')
    bookings = db.relationship('Booking', backref='event')
	
    def __repr__(self): #string print method
        return "<Name: {}>".format(self.name)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    num_tickets = db.Column(db.Integer)
    total_paid = db.Column(db.Float)
    booking_date = db.Column(db.DateTime, default=datetime.now)
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return "<Booking: {}>".format(self.text)