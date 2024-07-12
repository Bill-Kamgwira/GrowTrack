import sqlite3

# Create a connection to the database (or create if it doesn't exist)
conn = sqlite3.connect("user_registration.db")  # Replace with your desired filename

# Create a cursor object to execute SQL statements
cursor = conn.cursor()

# Define the SQL statement to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  farm_name TEXT NOT NULL,
  region TEXT NOT NULL,
  traditional_authority TEXT NOT NULL,
  farm_size FLOAT NOT NULL
);
"""

# Execute the SQL statement using the cursor
cursor.execute(create_table_sql)

# Commit the changes to the database
conn.commit()

# Close the connection (optional, good practice)
conn.close()
