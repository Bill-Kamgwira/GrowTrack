# SQLAlchemy Instance Is Imported
from supdb import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users1"
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
    crops = db.relationship('Crop', back_populates='user')
    
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    planting_date = db.Column(db.Date)
    expected_harvest_date = db.Column(db.Date)
    crop_variety = db.Column(db.String(100))
    acreage = db.Column(db.Float)
    crop_rotation_history = db.Column(db.Text)  # Store as text for flexibility
    user_id = db.Column(db.Integer, db.ForeignKey('users1.id'))
    user = db.relationship('User', back_populates='crops')
    crop_management_records = db.relationship('CropManagement', back_populates='crop')
    yield_data = db.relationship('YieldData', backref='crop')
    financial_data = db.relationship('FinancialData', backref='crop', uselist=False)  # One-to-one relationship

class CropManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'))
     # Specific fields for different management types
     #Specific data for fertilization
    fertilizer_type = db.Column(db.String(50))
    fertilizer_amount = db.Column(db.Float)
    fertilizer_date = db.Column(db.Date)
    #Specific data for irrigation
    irrigation_type = db.Column(db.String(50))
    irrigation_amount = db.Column(db.Float)
    irrigation_amount = db.Column(db.Date)
    # Specifc data for Pest & Disease Control
    control_type = db.Column(db.String(50))
    control_amount = db.Column(db.Float)
    control_date = db.Column(db.Date)
    # Specific data for Weeding practices
    weeding_method = db.Column(db.String(50))
    weeding_date = db.Column(db.Date)
    # Specific data for Labour inputs
    tasks_completed = db.Column(db.String(200))
    hours_accrued = db.Column(db.Float)
    labour_date = db.Column(db.Date)
    
    crop = db.relationship('Crop')

class YieldData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'))
    quantity = db.Column(db.Float)
    quality = db.Column(db.String(50))
    harvest_date = db.Column(db.Date)
    post_harvest_loss = db.Column(db.Float)
    factors_affecting_yield = db.Column(db.Text)

class FinancialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id'), unique=True)  # One-to-one relationship
    seed_cost = db.Column(db.Float)
    fertilizer_cost = db.Column(db.Float)
    labor_cost = db.Column(db.Float)
    equipment_cost = db.Column(db.Float)
    pesticide_cost = db.Column(db.Float)
    revenue = db.Column(db.Float)

