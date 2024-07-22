# SQLAlchemy Instance Is Imported
from supdb import db

class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    farm_name = db.Column(db.String(255), nullable=False)
    region = db.Column(db.String(255), nullable=False)
    traditional_authority = db.Column(db.String(255), nullable=False)
    farm_size = db.Column(db.Float, nullable=False)
