import sqlite3

def connect_db():
  """
  Connects to the user registration database.
  """
  conn = sqlite3.connect("user_registration.db")
  return conn, conn.cursor()

def insert_user(cursor, username, email, password_hash, farm_name, region, traditional_authority, farm_size):
  """
  Inserts a new user into the database.

  Args:
      cursor (sqlite3.Cursor): Database cursor object.
      username (str): User's chosen username.
      email (str): User's email address.
      password_hash (str): Hashed password.
      farm_name (str): User's farm name.
      region (str): User's farm region.
      traditional_authority (str): User's traditional authority.
      farm_size (float): User's farm size.
  """

  insert_user_sql = """
  INSERT INTO users (username, email, password_hash, farm_name, region, traditional_authority, farm_size)
  VALUES (?, ?, ?, ?, ?, ?, ?)
  """

  try:
    user_data = (username, email, password_hash, farm_name, region, traditional_authority, farm_size)
    cursor.execute(insert_user_sql, user_data)
  except sqlite3.Error as error:
    print("An error occurred:", error)

# ... other database interaction functions 

