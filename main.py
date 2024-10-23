from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
from supdb import db
from models import User, Crop, CropManagement, YieldData, FinancialData, CropCycle
import secrets
from flask_migrate import Migrate
from flask_csv import send_csv
from bokeh.embed import components
from bokeh.plotting import figure
from datetime import datetime, date, timedelta
from collections import defaultdict
from bokeh.models import DatetimeTickFormatter, ColumnDataSource, DataRange1d
from math import pi
from bokeh.transform import cumsum
from bokeh.layouts import column
from bokeh.palettes import Spectral5
import pandas as pd





app = Flask(__name__, static_url_path='/static')


app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  

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

        # Check if username already exists
        existing_user_by_username = User.query.filter_by(username=username).first()
        if existing_user_by_username:
            errors.append(f"Username '{username}' is already taken.")

        # Check if email already exists
        existing_user_by_email = User.query.filter_by(email=email).first()
        if existing_user_by_email:
            errors.append(f"An account with the email '{email}' already exists.")

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
        
        # Confirm Password Validation
        if password != confirm_password:
            errors.append("Passwords do not match.")

        # Email validation using regular expressions
        email_regex = r"^\w+@\w+\.\w+$"
        if not re.match(email_regex, email):
            errors.append("Invalid email format. Please enter a valid email address (e.g., user@example.com).")

        # Farm name validation
        if not farm_name:
            errors.append("Farm name cannot be empty.")

        # Region and traditional authority validation
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Check if the account is locked
            if user.failed_attempts >= 5:
                # Cooldown of 15 minutes before allowing another login attempt
                cooldown_time = timedelta(minutes=15)
                if datetime.utcnow() - user.last_failed_attempt < cooldown_time:
                    flash('Account locked due to too many failed login attempts. Try again later.', 'error')
                    return render_template('login.html')

            # Check the password
            if check_password_hash(user.password_hash, password):
                # Reset failed login attempts after successful login
                user.failed_attempts = 0
                db.session.commit()

                #Mark session as permanent to activate timeout
                session.permanent = True

                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                # Incorrect password: increment failed attempts and set last_failed_attempt
                user.failed_attempts += 1
                user.last_failed_attempt = datetime.utcnow()
                db.session.commit()
                flash('Login Failed! Incorrect password.', 'error')
        else:
            flash('Login Failed! Invalid email or password.', 'error')
    
    return render_template('login.html')

#Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#Function to ensure that a datatime object is being returned
def ensure_datetime(date_obj):
    if date_obj is None:
        return None  # In case the date is None, return None
    if isinstance(date_obj, datetime):
        return date_obj  # Return directly if it's already a datetime object
    elif isinstance(date_obj, date):  # Convert date to datetime
        return datetime.combine(date_obj, datetime.min.time())
    elif isinstance(date_obj, str):  # If it's a string, try parsing it
        try:
            return datetime.strptime(date_obj, "%Y-%m-%d")
        except ValueError as e:
            print(f"Error parsing date string {date_obj}: {e}")
            return None  # Handle the error and return None
    return None  # Return None if no valid conversion could be made

#Route for Dahsboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch all cycles
    all_cycles = CropCycle.query.all()

    # Initialize dataframes
    fertilizer_df = pd.DataFrame(columns=['date', 'amount'])
    irrigation_df = pd.DataFrame(columns=['date', 'amount'])
    yield_df = pd.DataFrame(columns=['harvest_date', 'quantity'])
    financial_df = pd.DataFrame(columns=['cost_type', 'amount'])

    # Loop through cycles
    for cycle in all_cycles:
        cycle_id = cycle.id

        # Fetch and concatenate management data
        fertilizer_data = CropManagement.query.filter_by(crop_cycle_id=cycle_id, management_type='fertilization').all()
        if fertilizer_data:
            fertilizer_df = pd.concat([fertilizer_df, pd.DataFrame([(m.date, m.amount) for m in fertilizer_data], columns=['date', 'amount'])])

        irrigation_data = CropManagement.query.filter_by(crop_cycle_id=cycle_id, management_type='irrigation').all()
        if irrigation_data:
            irrigation_df = pd.concat([irrigation_df, pd.DataFrame([(m.date, m.amount) for m in irrigation_data], columns=['date', 'amount'])])

        # Fetch and concatenate yield data
        yield_data = YieldData.query.filter_by(crop_cycle_id=cycle_id).all()
        if yield_data:
            yield_df = pd.concat([yield_df, pd.DataFrame([(y.harvest_date, y.quantity) for y in yield_data], columns=['harvest_date', 'quantity'])])

        # Fetch and concatenate financial data
        financial_data = FinancialData.query.filter_by(crop_cycle_id=cycle_id).all()
        if financial_data:
            financial_df = pd.concat([financial_df, pd.DataFrame([(f.cost_type, f.amount) for f in financial_data], columns=['cost_type', 'amount'])])

    # Convert date columns to datetime
    if not fertilizer_df.empty:
        fertilizer_df['date'] = pd.to_datetime(fertilizer_df['date'], errors='coerce')

    if not irrigation_df.empty:
        irrigation_df['date'] = pd.to_datetime(irrigation_df['date'], errors='coerce')

    if not yield_df.empty:
        yield_df['harvest_date'] = pd.to_datetime(yield_df['harvest_date'], errors='coerce')

    # Only create charts if data exists
    layout = []

    if not fertilizer_df.empty:
        fertilizer_source = ColumnDataSource(fertilizer_df)
        fertilizer_fig = figure(title="Fertilizer Usage Over Time", x_axis_type='datetime')
        fertilizer_fig.line(x='date', y='amount', source=fertilizer_source, color='green')
        layout.append(fertilizer_fig)

    if not irrigation_df.empty:
        irrigation_source = ColumnDataSource(irrigation_df)
        irrigation_fig = figure(title="Irrigation Usage Over Time", x_axis_type='datetime')
        irrigation_fig.line(x='date', y='amount', source=irrigation_source, color='blue')
        layout.append(irrigation_fig)

    if not yield_df.empty and not fertilizer_df.empty:
        fertilizer_vs_yield_df = pd.merge(fertilizer_df, yield_df, left_on='date', right_on='harvest_date', how='inner')
        fertilizer_vs_yield_source = ColumnDataSource(fertilizer_vs_yield_df)
        fertilizer_vs_yield_fig = figure(title="Fertilizer vs Yield")
        fertilizer_vs_yield_fig.scatter(x='amount', y='quantity', source=fertilizer_vs_yield_source, color='green')
        layout.append(fertilizer_vs_yield_fig)

    if not yield_df.empty and not irrigation_df.empty:
        irrigation_vs_yield_df = pd.merge(irrigation_df, yield_df, left_on='date', right_on='harvest_date', how='inner')
        irrigation_vs_yield_source = ColumnDataSource(irrigation_vs_yield_df)
        irrigation_vs_yield_fig = figure(title="Irrigation vs Yield")
        irrigation_vs_yield_fig.scatter(x='amount', y='quantity', source=irrigation_vs_yield_source, color='blue')
        layout.append(irrigation_vs_yield_fig)

    if not financial_df.empty:
        financial_summary_df = financial_df.groupby('cost_type').sum().reset_index()
        financial_source = ColumnDataSource(financial_summary_df)
        financial_fig = figure(x_range=financial_summary_df['cost_type'], title="Financial Breakdown")
        financial_fig.vbar(x='cost_type', top='amount', source=financial_source, width=0.9)
        layout.append(financial_fig)

    # Generate the script and div for embedding in the HTML template
    script, div = components(layout)

    return render_template('dashboard.html', script=script, div=div)

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
            crop_variety=request.form['crop_variety'],
            acreage=float(request.form['acreage']),  # Ensure this is float
            user=current_user
        )
        db.session.add(crop)
        db.session.commit()
        flash('Crop added successfully!', 'success')
        return redirect(url_for('add_cycle', crop_id=crop.id))
    return render_template('add_crop.html')




@app.route('/add_cycle/<int:crop_id>', methods=['GET', 'POST'])
@login_required
def add_cycle(crop_id):
    # Fetch the crop from the database
    crop = Crop.query.get(crop_id)  # Fetch the specific crop based on crop_id

    if request.method == 'POST':
        cycle_name = request.form.get('cycle_name')  # Use get() to avoid KeyError

        # Get the planting and harvest date from the form
        planting_date = request.form.get('planting_date')
        harvest_date = request.form.get('harvest_date')

        # Convert the date input into a text format
        planting_date_str = str(planting_date)  # Already in 'YYYY-MM-DD' string format
        harvest_date_str = str(harvest_date) if harvest_date else None  # Convert to string if provided

        # Create the CropCycle object with the text values
        new_cycle = CropCycle(
            cycle_name=cycle_name,
            planting_dates=planting_date_str,
            harvest_dates=harvest_date_str,
            crop_id=crop_id
        )

        db.session.add(new_cycle)
        db.session.commit()

        flash('New cycle added successfully!', 'success')
        return redirect(url_for('view_crop', crop_id=crop_id))

    # Render the add cycle form
    return render_template('add_cycle.html', crop_id=crop_id, crop = crop)



# Route to View Crops added
@app.route('/view_crops', methods=['GET', 'POST'])
@login_required
def view_crops():
    crops = current_user.crops
    return render_template('view_crops.html', crops=crops)

# Route To view in depth crop management details
@app.route('/crop/<int:crop_id>')
@login_required
def view_crop(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    
    # Fetch the crop cycles for the crop
    crop_cycles = CropCycle.query.filter_by(crop_id=crop_id).all()
    
    # Initialize empty lists for management, yield, and financial records
    crop_management_records = []
    yield_production_records = []
    financial_data_records = []
    
    # Collect records from all cycles
    for cycle in crop_cycles:
        crop_management_records.extend(CropManagement.query.filter_by(crop_cycle_id=cycle.id).all())
        yield_production_records.extend(YieldData.query.filter_by(crop_cycle_id=cycle.id).all())
        financial_data_records.extend(FinancialData.query.filter_by(crop_cycle_id=cycle.id).all())
    
    return render_template('info.html', crop=crop, crop_cycles=crop_cycles,
                           crop_management_records=crop_management_records, 
                           yield_production_records=yield_production_records, 
                           financial_data_records=financial_data_records)

# Route for capturing Crop-management data on the crop cycle
@app.route('/crop/<int:crop_id>/cycle/<int:cycle_id>/add-management', methods=['GET', 'POST'])
@login_required
def add_crop_management(crop_id, cycle_id):
    crop = Crop.query.get_or_404(crop_id)
    crop_cycle = CropCycle.query.get_or_404(cycle_id)

    if request.method == 'POST':
        management_type = request.form.get('management_type')  # Get management type (fertilization, irrigation, etc.)
        amount = request.form.get('amount')  # General amount field for fertilizer, irrigation, etc.
        date = request.form.get('date')  # Date of the management event
        details = request.form.get('details')  # Additional details like fertilizer type, weeding method, etc.

        # Create the crop management record using the new schema structure
        management_record = CropManagement(
            crop_cycle_id=crop_cycle.id,
            management_type=management_type,
            amount=float(amount) if amount else None,  # Convert to float if present
            date=datetime.strptime(date, '%Y-%m-%d').date() if date else None,
            details=details  # Store extra details like fertilizer type, etc.
        )

        db.session.add(management_record)
        db.session.commit()
        flash('Crop management record added successfully!', 'success')
        return redirect(url_for('view_crop', crop_id=crop_id, cycle_id=cycle_id))

    return render_template('add_crop_management.html', crop=crop, crop_cycle=crop_cycle)


# Route for capturing yield & production on the crop cycle
@app.route('/crop/<int:crop_id>/cycle/<int:cycle_id>/add-yield_production', methods=['GET', 'POST'])
@login_required
def add_YieldData(crop_id, cycle_id):
    crop = Crop.query.get_or_404(crop_id)
    crop_cycle = CropCycle.query.get_or_404(cycle_id)

    if request.method == 'POST':
        yield_production = YieldData(
            quantity=float(request.form['yield-quantity']),
            quality=request.form['yield-quality'],
            harvest_date=datetime.strptime(request.form['harvest_date'], '%Y-%m-%d').date(),
            crop_cycle_id=crop_cycle.id  # Link yield data to the specific crop cycle
        )

        db.session.add(yield_production)
        db.session.commit()
        flash('Yield data added successfully!', 'success')
        return redirect(url_for('view_crop', crop_id=crop_id, cycle_id=cycle_id))

    return render_template('add_yield_production.html', crop=crop, crop_cycle=crop_cycle)


# Route for capturing financial data on the crop cycle
@app.route('/crop/<int:crop_id>/cycle/<int:cycle_id>/add-financial', methods=['GET', 'POST'])
@login_required
def add_FinanceData(crop_id, cycle_id):
    crop = Crop.query.get_or_404(crop_id)
    crop_cycle = CropCycle.query.get_or_404(cycle_id)

    if request.method == 'POST':
        # Assuming the form provides multiple types of financial data entries (e.g., seed, fertilizer, etc.)
        cost_type = request.form['cost_type']  # Type of cost ('Seed', 'Fertilizer', etc.)
        amount = float(request.form['amount'])  # The amount for the cost/revenue
        details = request.form.get('details', '')  # Additional optional details
        date = request.form['date']  # Date when the cost/revenue was recorded

        financial_data = FinancialData(
            cost_type=cost_type,
            amount=amount,
            details=details,
            date=datetime.strptime(date, '%Y-%m-%d'),  # Converting string to date object
            crop_cycle_id=crop_cycle.id  # Link financial data to the specific crop cycle
        )

        db.session.add(financial_data)
        db.session.commit()
        flash('Financial data added successfully!', 'success')
        return redirect(url_for('view_crop', crop_id=crop_id, cycle_id=cycle_id))

    return render_template('add_financial.html', crop=crop, crop_cycle=crop_cycle)



@app.route('/export/csv/<int:crop_id>/crop_manage')
def export_crop_manage_data(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    crop_management_records = CropManagement.query.join(CropCycle).filter(CropCycle.crop_id == crop_id).all()

    # Prepare the data list to store rows for the CSV
    data = []

    for record in crop_management_records:
        filtered_record = {
            'management_type': record.management_type or "",
            'amount': record.amount or "",
            'date': record.date.strftime('%Y-%m-%d') if record.date else "",  # Format the date to a readable string
            'details': record.details or "",
        }
        data.append(filtered_record)

    # Define the CSV header fields
    fields = ['management_type', 'amount', 'date', 'details']

    # Use send_csv to generate and return the CSV response
    return send_csv(data, f"{crop.name}_CropManagement.csv", fields=fields)


@app.route('/export/csv/<int:crop_id>/yield_data')
def export_yield_data(crop_id):
    crop = Crop.query.get_or_404(crop_id)
    
    # Query yield data by joining through CropCycle based on crop_id
    yield_data_records = YieldData.query.join(CropCycle).filter(CropCycle.crop_id == crop_id).all()

    data = []
    for record in yield_data_records:

        
        # Create the filtered yield data dictionary
        yield_data_fields = {
            'quantity': record.quantity or "",
            'quality': record.quality or "",
            'harvest_date':record.harvest_date,  # Assuming this is a string or JSON field
        }
        data.append(yield_data_fields)

    # Define the CSV header fields
    fields = ['quantity', 'quality', 'harvest_date']

    # Generate and return the CSV
    return send_csv(data, f"{crop.name}_yield_data.csv", fields=fields)


@app.route('/export/csv/<int:crop_id>/financial_data')
def export_financial_data(crop_id):
    crop = Crop.query.get_or_404(crop_id)

    # Query financial data by joining through CropCycle based on crop_id
    financial_data_records = FinancialData.query.join(CropCycle).filter(CropCycle.crop_id == crop_id).all()

    # Initialize a dictionary to store financial data grouped by cycle and type
    data = []
    for record in financial_data_records:
        # Create a dictionary for each record with cost_type and amount
        financial_data_fields = {
            'cost_type': record.cost_type or "",
            'amount': record.amount or "",
            'details': record.details or "",  # Add details if necessary
            'date': record.date.strftime('%Y-%m-%d') if record.date else ""
        }
        data.append(financial_data_fields)

    # Define the CSV header fields
    fields = ['cost_type', 'amount', 'details', 'date']

    # Generate and return the CSV
    return send_csv(data, f"{crop.name}_financial_data.csv", fields=fields)



@app.route('/delete_crop/<int:crop_id>', methods=['POST'])
@login_required
def delete_crop(crop_id):
    # Query the crop by ID
    crop = db.session.query(Crop).filter_by(id=crop_id, user_id=current_user.id).first()

    if not crop:
        flash("Crop not found or you don't have permission to delete this crop.", "danger")
        return redirect(url_for('dashboard'))

    try:
        # Delete related data (CropCycle, YieldData, CropManagement, FinancialData) before deleting the crop
        for cycle in crop.cycles:
            db.session.query(CropManagement).filter_by(crop_cycle_id=cycle.id).delete()
            db.session.query(YieldData).filter_by(crop_cycle_id=cycle.id).delete()
            db.session.query(FinancialData).filter_by(crop_cycle_id=cycle.id).delete()

        # Finally delete crop cycles and the crop itself
        db.session.query(CropCycle).filter_by(crop_id=crop.id).delete()
        db.session.delete(crop)
        db.session.commit()

        flash(f"Crop '{crop.name}' and its related data have been deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the crop.", "danger")
    
    return redirect(url_for('dashboard'))


# Run the development server (add this outside any functions)
if __name__ == "__main__":
  create_db()
  app.run(debug=True)  # Run the development server in debug mode
  
