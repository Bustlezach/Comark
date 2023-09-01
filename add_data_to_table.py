import sqlite3
import csv

# Connect to the SQLite database
conn = sqlite3.connect('C:\\Users\\hp\\Documents\\Comark\\instance\\comark.db')
cursor = conn.cursor()

# Replace 'your_table' with the actual table name
table_name = 'products'

# CSV file containing your data
csv_file = 'C:\\Users\\hp\\Documents\\Comark\\raw_data.csv'

# Open and read the CSV file with explicit encoding (e.g., UTF-8)
with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader)  # Skip the header row if present

    for row in csv_reader:
        # Assuming your CSV columns correspond to your table columns
        # Replace the placeholders with the actual column names
        cursor.execute(f"INSERT INTO {table_name} (product_id, product_name, category, price, description, img_link, user_id, username) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)

# Commit the changes and close the connection
conn.commit()
conn.close()
