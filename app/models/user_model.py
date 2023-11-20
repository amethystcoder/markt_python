from db import db
from passlib.hash import pbkdf2_sha256
import hashlib
import uuid


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(400), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(200))
    phone_number = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    user_type = db.Column(db.String(255), nullable=False)
    user_status = db.Column(db.String(255), default='active')
    # Add other common attributes here

    # Define a relationship with the Chat model
    chats = db.relationship('Chat', back_populates='user')
    
    def __init__(self,*args, **kwargs):
        """sumary_line
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        
        for key,value in kwargs.items():
            if key == "create_new":
                self.email = kwargs["email"]
                self.password = self.set_password(kwargs["password"])
                self.profile_picture = kwargs["profile_picture"]
                self.phone_number = kwargs["phone_number"]
                self.longitude = kwargs["longitude"]
                self.latitude = kwargs["latitude"]
                self.house_number = kwargs["house_number"]
                self.street = kwargs["street"]
                self.city = kwargs["city"]
                self.state = kwargs["state"]
                self.country = kwargs["country"]
                self.postal_code = kwargs["postal_code"]
                self.user_type = kwargs["user_type"]
            if key == "get_user_by_email":
                self.email = kwargs["email"]
                self.password = kwargs["password"]
                self = self.get_user_using_email(self.email)
            if key == "get_user_by_phone":
                self.phone_number = kwargs["phone_number"]
                self.password = kwargs["password"]
                self = self.get_user_using_phone(self.phone_number)
            if key == "password_change_reset":
                self.email = kwargs["email"]
                self.phone_number = kwargs["phone_number"]

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def generate_unique_id():
        unique_id = str(uuid.uuid4()).encode()
        return hashlib.sha256(unique_id).hexdigest()
    
    def get_reset_user_using_email_or_phone(self,email,phone):
        if email is not None:
            return db.session.query(User).filter(User.email == email).first()
        elif phone is not None:
            return db.session.query(User).filter(User.phone_number == phone).first()
        return None
        
    def get_user_using_email(self,email):
        user = db.session.query(User).filter(User.email == email).first()
        if user is not None:
            if self.check_password(user.password):
                return user
            return None
        return None
    
    def get_user_using_phone(self,phone):
        user = db.session.query(User).filter(User.phone_number == phone).first()
        if user is not None:
            if self.check_password(user.password):
                return user
            return None
        return None

    def set_password(self, password):
        self.password = pbkdf2_sha256.hash(password)
        
    def change_password(self, password):
        self.password = pbkdf2_sha256.hash(password)
        db.session.commit()
        
    def get_user_location_data(self,unique_id):
        data = db.session.query(User).filter(User.unique_id == unique_id).first()
        return {
            "city":data.city,
            "country":data.country,
            "longitude":data.longitude,
            "latitude":data.latitude,
            "house_number":data.house_number,
            "state":data.state,
            "street":data.street,
            "postal_code":data.postal_code
            }

    def check_password(self, password): 
        return pbkdf2_sha256.verify(password, self.password)

    def change_status(self,status):
        acceptable_status = ["active","offline","standby"] #standby could be a status for when user is online but not on present screen
        if status in acceptable_status:
            self.user_status = status
            db.session.commit()