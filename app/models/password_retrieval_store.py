import time
from db import db

class PasswordRetrievalData(db.model):
    __tablename__ = "buyers"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    recovery_code = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(400), nullable=False, unique=True)
    email = db.Column(db.String(400), nullable=False, unique=True)
    expiration_time = db.Column(db.TIMESTAMP, default=time.time() + (60 * 10), nullable=False)
    
    def __init__(self,user_id,email,recovery_code):
        if user_id is None and recovery_code is None:
            if email is not None:
                self = self.get_recovery_data(email=email)
        else:
            self.user_id = user_id
            self.email = email
            self.recovery_code = recovery_code
        
    def is_expired(self):
        if self.recovery_code < time.time(): 
            self.delete_from_db()
            return True
        return False
    
    def is_code_right(self,code):
        return code == self.recovery_code
    
    @classmethod
    def get_all_other_recovery_attempts(self,email):
        return db.session.query(PasswordRetrievalData).filter(PasswordRetrievalData.email == email).count()
    
    @classmethod
    def get_recovery_data(self,email):
        return db.session.query(PasswordRetrievalData).filter(PasswordRetrievalData.email == email).first()
    
    @classmethod
    def delete_all_other_recovery_attempts(self,email):
        return db.session.query(PasswordRetrievalData).filter(PasswordRetrievalData.email == email).delete(synchronize_session=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    # Add Buyer-specific methods here
