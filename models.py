from supdb import db
from flask_login import UserMixin
from datetime import datetime

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(db.Model, UserMixin, TimestampMixin):
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
    failed_attempts = db.Column(db.Integer, default=0, nullable=False)
    last_failed_attempt = db.Column(db.DateTime, nullable=True)
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

class Crop(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    crop_variety = db.Column(db.String(100))
    acreage = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users1.id', name='fk_crop_user_id'))  # Named constraint
    user = db.relationship('User', back_populates='crops')
    cycles = db.relationship('CropCycle', back_populates='crop')  # Link to CropCycle

class CropCycle(db.Model, TimestampMixin):
    __tablename__ = 'cropcycle'  # Ensures that the table name is exactly 'cropcycle'
    id = db.Column(db.Integer, primary_key=True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.id', name='fk_cropcycle_crop_id'))  # Named constraint
    crop = db.relationship('Crop', back_populates='cycles')
    cycle_name = db.Column(db.String(100))  # Optional name for each cycle
    planting_dates = db.Column(db.Text)  # Storing multiple dates as text (could be JSON format)
    harvest_dates = db.Column(db.Text)  # Storing multiple harvest dates
    crop_management_records = db.relationship('CropManagement', back_populates='cycle')
    yield_data = db.relationship('YieldData', back_populates='cycle')
    financial_data = db.relationship('FinancialData', back_populates='cycle')

class CropManagement(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    crop_cycle_id = db.Column(db.Integer, db.ForeignKey('cropcycle.id', name='fk_cropmanagement_crop_cycle_id'))  # Named constraint
    cycle = db.relationship('CropCycle', back_populates='crop_management_records')
    
    # New structure
    management_type = db.Column(db.String(50))  # Example values: 'Fertilizer', 'Irrigation', 'Control', 'Weeding', 'Labour'
    amount = db.Column(db.Float, nullable=True)  # For things like fertilizer amount, irrigation amount, etc.
    date = db.Column(db.Date, nullable=True)  # Date when the activity was done
    details = db.Column(db.String(200), nullable=True)  # Further details, e.g., the type of fertilizer or weeding method
    
    # Any extra fields that might be common to all management types can go here


class YieldData(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    crop_cycle_id = db.Column(db.Integer, db.ForeignKey('cropcycle.id', name='fk_yielddata_crop_cycle_id'))  # Named constraint
    cycle = db.relationship('CropCycle', back_populates='yield_data')
    quantity = db.Column(db.Float)
    quality = db.Column(db.String(50))
    harvest_dates = db.Column(db.Text)  # Multiple harvest events

class FinancialData(db.Model, TimestampMixin):
    id = db.Column(db.Integer, primary_key=True)
    crop_cycle_id = db.Column(db.Integer, db.ForeignKey('cropcycle.id', name='fk_financialdata_crop_cycle_id'))  # Named constraint
    cycle = db.relationship('CropCycle', back_populates='financial_data')
    seed_cost = db.Column(db.Float)
    fertilizer_cost = db.Column(db.Float)
    labor_cost = db.Column(db.Float)
    equipment_cost = db.Column(db.Float)
    pesticide_cost = db.Column(db.Float)
    revenue = db.Column(db.Float)
