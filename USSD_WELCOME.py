from colorama import Fore, Style
import re
import getpass

ascii_art = """
   _____                 _______             _    
  / ____|               |__   __|           | |   
 | |  __ _ __ _____      __| |_ __ __ _  ___| | __
 | | |_ | '__/ _ \ \ /\ / /| | '__/ _` |/ __| |/ /
 | |__| | | | (_) \ V  V / | | | | (_| | (__|   < 
  \_____|_|  \___/ \_/\_/  |_|_|  \__,_|\___|_|\_\ 

"""
max_width = 10  # Adjust this value based on your desired width
min_length = 8
centered_ascii_art = ascii_art.splitlines()  # Split into lines
centered_ascii_art = [line.center(max_width) for line in centered_ascii_art]  # Center each line
centered_ascii_art = '\n'.join(centered_ascii_art)  # Join lines back with newlines

welcome_message = f"""
{centered_ascii_art}

{''.center(max_width, ' ')}Welcome to GrowTrack!

{''.center(max_width, ' ')}Please choose an option:

{''.center(max_width, ' ')}{Fore.GREEN}1. Login{Style.RESET_ALL}
{''.center(max_width, ' ')}{Fore.BLUE}2. Register{Style.RESET_ALL}
"""

user_choice = input(welcome_message)

# Validate user input
while user_choice not in ("1", "2"):
    print("Invalid input. Please enter 1 or 2.")
    user_choice = input("Enter your choice again: ")

# Process user choice
if user_choice == "1":
  print("Login initiated...")
  exit() 
  # Registration functionality
elif user_choice == "2":
  print("Registration initiated...")

  while True:
    username = input("Enter username: ")
    if username:  # Check if username is not empty (truthy in Python)
      break  # Exit the loop if username is valid
    else:
      print("Username cannot be empty. Please try again.")

  while True:
    password = getpass.getpass("Enter password: ")  # Use getpass for hidden input

    if len(password) < min_length: # Check length
      print(f"Password must be at least {min_length} characters long.")
      continue  # Skip to the next iteration of the loop

    # Check password complexity (at least one of each)
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_symbol = any(not char.isalnum() for char in password)  # Exclude alphanumeric characters

    complexity_requirements_met = has_uppercase and has_lowercase and (has_digit or has_symbol)
    if not complexity_requirements_met:
      print("Password must contain at least one uppercase letter, one lowercase letter, one number, and one symbol.")
      continue  # Skip to the next iteration of the loop

    # Prompt for confirmation and validate
    password_confirmation = getpass.getpass("Confirm password: ")
    if password != password_confirmation:
      print("Passwords do not match. Please try again.")
      continue  # Skip to the next iteration of the loop

    # All requirements met, break out of the loop
    break

  while True:
    email = input("Enter email address: ")
  # Validate email format using regular expressions
  
    email_regex = r"^\w+@\w+\.\w+$"
    if re.match(email_regex, email):
      break  # Exit the loop if email is valid
    else:
      print("Invalid email format. Please enter a valid email address (e.g., user@example.com).")

  while True:
    farm_name = input("Enter your Farm name: ")
    if farm_name:
      break
    else:
      print("Farm name cannot be empty. Please try again.")

# Region and Traditional Authority (assuming separate inputs)
  while True:
    region = input("Enter your region: ")
    if region:
      break
    else:
      print("Region cannot be empty. Please try again.")

  while True:
    ta = input("Enter your Traditional Authority: ")
    if ta:
      break
    else:
      print("Traditional Authority cannot be empty. Please try again.")

  while True:
    farm_size = input("Enter farm size (in hectares): ")
    if not farm_size:  # Check for empty input
      print("Farm size cannot be empty. Please enter a value.")
      continue
    try:
      farm_size = float(farm_size)
      if farm_size <= 0:
          print("Farm size must be a positive number. Please enter a value greater than zero.")
          continue
    except ValueError:
      print("Invalid farm size. Please enter a number.")
      continue
  # Farm size is valid (positive float), proceed...
    break

  print("\n Processing registration...")

  exit() 
  # Add your registration functionality here
else:
  print("Unexpected error occurred.")  # Handle unexpected input
  exit() 

