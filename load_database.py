import sqlite3
import csv

# Define files to upload path
software_company_path = 'example/software_development_google_maps_data.csv'
software_company_location_path = 'example/software_location.csv'

# Define database file path
db_file = "data/software_companies.db"

# Connect or create the database file
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Drop existing tables if they exist (for script re-running)
cursor.execute("DROP TABLE IF EXISTS software_company")
cursor.execute("DROP TABLE IF EXISTS software_location")

# Create software_company table
cursor.execute("""CREATE TABLE software_company (
                    name TEXT,
                    rating TEXT,
                    address TEXT,
                    postcode TEXT,
                    web TEXT,
                    phone TEXT
                )""")

# Create software_location table with indexed latitude and longitude
cursor.execute("""CREATE TABLE software_location (
                    postcode TEXT PRIMARY KEY,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL
                )""")

# Function to insert data into software_company table
def insert_company_data(data):
    cursor.execute("""INSERT INTO software_company (
                        name, rating, address, postcode, web, phone
                    ) VALUES (?, ?, ?, ?, ?, ?)""", data)


# Function to insert data into software_location table
def insert_location_data(data):
    postcode = data[0]
    cursor.execute("SELECT EXISTS(SELECT 1 FROM software_location WHERE postcode=?)", (postcode,))
    exists = cursor.fetchone()[0]
    
    if not exists:
        cursor.execute("""INSERT INTO software_location (
                            postcode, latitude, longitude
                        ) VALUES (?, ?, ?)""", data)


# Function to upload CSV data to the database
def upload_csv_to_database(file_path, insert_data_function):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)  # Skip header row

        for row in reader:
            # Clean data (remove special characters and trim whitespace)
            clean_data = [cell.strip() for cell in row]

            # Insert data into the appropriate table
            insert_data_function(clean_data)


# Upload software company data
upload_csv_to_database(software_company_path, insert_company_data)

# Upload software location data
upload_csv_to_database(software_company_location_path, insert_location_data)

# Commit transactions and close the connection
conn.commit()
conn.close()
