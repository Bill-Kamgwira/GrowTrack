from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash # for password hashing
import re

app = Flask(__name__)

users = []

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
            # ... user storage logic (replace with database interaction)
            users.append({
                "username": username,
                "password_hash": hashed_password,
                "email": email,
                "farm_name": farm_name,
                "region": region,
                "traditional_authority": traditional_authority,
                "farm_size": farm_size,
            })
            return "User Registered!"  # Placeholder for success message (replace later)


# Run the development server (add this outside any functions)
if __name__ == "__main__":
  app.run(debug=True)  # Run the development server in debug mode
