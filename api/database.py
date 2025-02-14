import os
import sqlite3
import csv

DATABASE_PATH = 'mice.db'
CSV_PATH = 'mice.csv'

def create_database():
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)

    # connect to SQLite
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # create table "mice" with all fields from CSV
    cursor.execute('''
        CREATE TABLE mice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            length REAL,
            width REAL,
            weight REAL,
            shape TEXT,
            connectivity TEXT,
            sensor TEXT,
            dpi INTEGER,
            polling_rate INTEGER,
            side_buttons INTEGER,
            grip_type TEXT
        );
    ''')

# insert data from CSV into the table
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        mice_data = []
        for row in reader:
            # Convert length and width to cm (keep one decimal point)
            length_cm = round(float(row['Length (mm)']) / 10, 1)
            width_cm = round(float(row['Width (mm)']) / 10, 1)

            # Prepare row data for insertion
            mice_data.append((
                row['Name'],
                length_cm,
                width_cm,
                float(row['Weight (g)']),
                row['Shape'],
                row['Connectivity'],
                row['Sensor'],
                int(row['DPI']),
                int(row['Polling Rate']),
                int(row['Side Buttons']),
                row['Grip Type']
            ))

    # insert rows into the database
    cursor.executemany('''
        INSERT INTO mice (name, length, width, weight, shape, connectivity, sensor, dpi, polling_rate, side_buttons, grip_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', mice_data)

    # commit changes and close connection
    conn.commit()
    conn.close()

# create and populate the database if this script is run directly
if __name__ == '__main__':
    create_database()
