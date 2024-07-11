from colorama import Fore, Style

ascii_art = """
   _____                 _______             _    
  / ____|               |__   __|           | |   
 | |  __ _ __ _____      __| |_ __ __ _  ___| | __
 | | |_ | '__/ _ \ \ /\ / /| | '__/ _` |/ __| |/ /
 | |__| | | | (_) \ V  V / | | | | (_| | (__|   < 
  \_____|_|  \___/ \_/\_/  |_|_|  \__,_|\___|_|\_\ 

"""
max_width = 10  # Adjust this value based on your desired width

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
  # Add your login functionality here
elif user_choice == "2":
  print("Registration initiated...")

  username = input("Enter username: ")
  email = input("Enter email address: ")
  password = input("Enter password: ")
  farm_name = input("Enter your farm name: ")

# Region and Traditional Authority (assuming separate inputs)
  region = input("Enter your region: ")
  ta = input("Enter your Traditional Authority: ")

# Optional Geolocation (can be wrapped in a conditional block)
  geolocation = input("Enter your geolocation coordinates (optional): ")

  farm_size = input("Enter the size of your farm (hectares): ")

# Optional Soil Type and Irrigation System
  soil_type = input("Enter your soil type (optional): ")
  irrigation = input("Do you have an irrigation system? (yes/no): ").lower()  # convert to lowercase for easier comparison


  exit() 
  # Add your registration functionality here
else:
  print("Unexpected error occurred.")  # Handle unexpected input
  exit() 
