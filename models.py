# SQLAlchemy Instance Is Imported
from supdb import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    farm_name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    traditional_authority = db.Column(db.String(255), nullable=False)
    farm_size = db.Column(db.Float, nullable=False)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


