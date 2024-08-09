from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
from supdb import db
from models import User, Crop, CropManagement, YieldData, FinancialData
import secrets
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__, static_url_path='/static')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# Configure Flask-SQLAlchemy to use Session.get()
app.config['SQLALCHEMY_USE_GET_IDENTITY'] = True

db.init_app(app)  

migrate = Migrate(app, db)

# Creating Database with App Context
def create_db():
    with app.app_context():
        db.create_all()


#Login Manager Configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Directs users to the Login function.

# Generate a strong random secret key
app.config['SECRET_KEY'] = secrets.token_hex(32)

#Route for Landing page
@app.route('/')
def home():
    return render_template('landing.html')

# Route and logic for Signup functionality
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        farm_name = request.form["farm_name"]
        region = request.form["region"]
        traditional_authority = request.form["traditional_authority"]
        farm_size = request.form["farm_size"]
        confirm_password = request.form['confirm_password']

        errors = []  # List to store any validation errors

        # Username validation
        if not username:
            errors.append("Username cannot be empty.")

        # Password validation
        min_length = 8  # Adjust minimum length as needed
        if len(password) < min_length:
            errors.append(f"Password must be at least {min_length} characters long.")
        else:
            has_uppercase = any(char.isupper() for char in password)
            has_lowercase = any(char.islower() for char in password)
            has_digit = any(char.isdigit() for char in password)
            has_symbol = any(not char.isalnum() for char in password)
            complexity_requirements_met = has_uppercase and has_lowercase and (has_digit or has_symbol)
            if not complexity_requirements_met:
                errors.append("Password must contain at least one uppercase letter, one lowercase letter, one number, and one symbol.")
        
        #Confirm Password Validation
        if password != confirm_password:
            errors.append("Passwords do not match.")

        # Email validation using regular expressions
        email_regex = r"^\w+@\w+\.\w+$"
        if not re.match(email_regex, email):
            errors.append("Invalid email format. Please enter a valid email address (e.g., user@example.com).")

        # Farm name validation
        if not farm_name:
            errors.append("Farm name cannot be empty.")

        # Region and traditional authority validation (assuming separate inputs)
        if not region:
            errors.append("Region cannot be empty.")
        if not traditional_authority:
            errors.append("Traditional Authority cannot be empty.")

        # Farm size validation (positive float)
        try:
            farm_size = float(farm_size)
            if farm_size <= 0:
                errors.append("Farm size must be a positive number. Please enter a value greater than zero.")
        except ValueError:
            errors.append("Invalid farm size. Please enter a number.")

        if errors:  # Handle validation errors
            return render_template("signup.html", errors=errors)
        else:
            # All validation passed, proceed with user registration
            hashed_password = generate_password_hash(password)
            user = User(username=username, password_hash=hashed_password, email=email,
                    farm_name=farm_name, region=region, traditional_authority=traditional_authority,
                    farm_size=farm_size)
            db.session.add(user)  # Add user to the database session
            db.session.commit()  # Commit the changes to the database
            return redirect(url_for('login'))


@app.route('/view_users') #To view Contents of the Database
def view_users():
    users = User.query.all()  # Query all users
    return render_template('users.html', users=users)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            if not user:
                flash('Login Failed! Invalid email or password.', 'error')
            else:
                flash('Login Failed! Incorrect password.', 'error')
    return render_template('login.html')

#Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Dashboard Route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Route for User to view profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# Route for Editing User profiles
@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        # Add more fields to update as needed
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))
    return render_template('edit-profile.html', user=current_user)

# Route to Crop data capture form
@app.route('/add_crop', methods=['GET', 'POST'])
@login_required
def add_crop():
    if request.method == 'POST':
        crop = Crop(
            name=request.form['name'],
            planting_date = datetime.strptime(request.form['planting_date'], '%Y-%m-%d').date(),
            expected_harvest_date = datetime.strptime(request.form['expected_harvest_date'], '%Y-%m-%d').date(),
            crop_variety=request.form['crop_variety'],
            acreage=request.form['acreage'],
            crop_rotation_history=request.form['crop_rotation'],
            user=current_user
        )
        db.session.add(crop)
        db.session.commit()
        flash('Crop added successfully!', 'success')
        return redirect(url_for('view_crops'))
    return render_template('add_crop.html')

# Route to View Crops added
@app.route('/view_crops')
@login_required
def view_crops():
    crops = current_user.crops
    return render_template('view_crops.html', crops=crops)

# Route for link to view details of crops
@app.route('/crop/<int:crop_id>')
@login_required
def view_crop(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    crop_management_records = CropManagement.query.filter_by(crop_id=crop_id).all()
    yield_production_records = YieldData.query.filter_by(crop_id=crop_id).all()
    financial_data_records = FinancialData.query.filter_by(crop_id=crop_id).all()
    return render_template('info.html', crop=crop, crop_management_records=crop_management_records, yield_production_records=yield_production_records, financial_data_records = financial_data_records)

#Route for capturing Crop-management data on the crop
@app.route('/crop/<int:crop_id>/add-management', methods=['GET', 'POST'])
@login_required
def add_crop_management(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    if request.method == 'POST':
        management_type = request.form.get('management_type')
        management_data = {}

        if management_type == 'fertilization':
            management_data = {
            'fertilizer_type' : request.form.get('fertilizer_type'),
            'fertilizer_amount' : float(request.form.get('fertilizer_amount')),
            'fertilizer_date' : datetime.strptime(request.form.get('fertilizer_date'), '%Y-%m-%d').date(),
            }
        elif management_type == 'irrigation':
            management_data = {
            'irrigation_type' : request.form.get('irrigation_type'),
            'irrigation_amount' : float(request.form.get('irrigation_amount')),
            'irrigation_date' : datetime.strptime(request.form.get('irrigation_date'), '%Y-%m-%d').date(),
            }
        elif management_type == 'pest_control':
            management_data = {
            'control_type' : request.form.get('control_type'),
            'control_amount' : float(request.form.get('control_amount')),
            'control_date' : datetime.strptime(request.form.get('control_date'), '%Y-%m-%d').date(),
            }
        elif management_type == 'weeding':
            management_data = {
            'weeding_method' : request.form.get('weeding_method'),
            'weeding_date' : datetime.strptime(request.form.get('weeding_date'), '%Y-%m-%d').date(),
            }
        elif management_type == 'labor':
            management_data = {
            'tasks_completed' : request.form.get('tasks_completed'),
            'hours_accrued' : float(request.form.get('hours_accrued')),
            'labour_date' : datetime.strptime(request.form.get('labour_date'), '%Y-%m-%d').date(),
            }

        management_record = CropManagement(
            crop=crop,
            **management_data
        )
        db.session.add(management_record)
        db.session.commit()
        flash('Crop management record added successfully!', 'success')
        return redirect(url_for('view_crop', crop_id=crop_id))

    return render_template('add_crop_management.html', crop=crop)

#Route for capturing yield & production on the crop
@app.route('/crop/<int:crop_id>/add-yield_production', methods=['GET', 'POST'])
@login_required
def add_YieldData(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    if request.method == 'POST':
        
        yield_production = YieldData(
            quantity=float(request.form['yield-quantity']),
            quality=request.form['yield-quality'],
            harvest_date = datetime.strptime(request.form['harvest_date'], '%Y-%m-%d').date(),
            post_harvest_loss=float(request.form['post_harvest_losses']),
            factors_affecting_yield=request.form['factors'],
            crop = crop
        )
        db.session.add(yield_production)
        db.session.commit()
        flash('Yield data added successfully!', 'success')
        return redirect(url_for('view_crop', crop_id=crop_id)) 

    return render_template('add_yield_production.html', crop = crop)

#Route for capturing yield & production on the crop
@app.route('/crop/<int:crop_id>/add-financial', methods=['GET', 'POST'])
@login_required
def add_FinanceData(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    if request.method == 'POST':
        
        financial_data = FinancialData(
            seed_cost=float(request.form['seed-cost']),
            fertilizer_cost=float(request.form['fertilizer_cost']),
            labor_cost=float(request.form['labor_cost']),
            equipment_cost=float(request.form['equipment_cost']),
            pesticide_cost=float(request.form['pesticide_cost']),
            revenue=float(request.form['revenue']),
            crop = crop
        )
        db.session.add(financial_data)
        db.session.commit()
        flash('Financial data added successfully!', 'success')
        return redirect(url_for('view_crop', crop_id=crop_id)) 

    return render_template('add_financial.html', crop = crop)

# Run the development server (add this outside any functions)
if __name__ == "__main__":
  create_db()
  app.run(debug=True)  # Run the development server in debug mode
  
