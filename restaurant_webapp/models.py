from flask_login import UserMixin
from restaurant_webapp import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100), unique=True)

    def get_id(self):
        # this matches what user_loader needs to uniquely load a user
        return self.id
    
    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False

class reservation(UserMixin, db.Model):
    reservation_id = db.Column(db.Integer, primary_key=True)
    under_name = db.Column(db.Text, nullable=False)
    no_of_people = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Text, nullable=False)
    day = db.Column(db.Text, nullable=False)
