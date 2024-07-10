loreg = input("Welcome to GrowTrack! Press 1. To Login Press 2. To Register: ")

# Validate user input
while loreg not in ("1", "2"):
    print("Invalid input. Please enter 1 or 2.")
    loreg = input("Enter your choice again: ")

# Process user choice
if loreg == "1":
  print("Login initiated...")
  exit() 
  # Add your login functionality here
elif loreg == "2":
  print("Registration initiated...")
  exit() 
  # Add your registration functionality here
else:
  print("Unexpected error occurred.")  # Handle unexpected input
  exit() 
