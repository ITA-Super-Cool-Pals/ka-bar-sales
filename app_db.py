import sqlite3, os, csv

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app-db', 'bar_sales.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Create database
def db_create():
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        # Create table if it doesn't exist
        cur.execute("""CREATE TABLE IF NOT EXISTS bar_sales (
                    drinkId INTEGER PRIMARY KEY AUTOINCREMENT,
                    drinkName TEXT,
                    category TEXT,
                    priceDkk FLOAT,
                    unitsSold INTEGER
                    )""")

        # Read and insert data from CSV file
        with open('barSalesData.csv', 'r') as file:
            reader = csv.reader(file, delimiter=';') # Specify semicolon as delimiter
            next(reader) # Skip header row if present
            #rows = [(row[0], row[1], float(row[2]), int(row[3])) for row in reader]

            rows = []
            for row in reader:
                # Skip empty rows to avoid errors
                if not row or len(row) < 4:
                    continue

                # Replace comma with dot for decimal conversion
                drink_name = row[0]
                category = row[1]
                price_dkk = float(row[2].replace(',', '.'))
                units_sold = int(row[3])

                rows.append((drink_name, category, price_dkk, units_sold))

            # Insert rows into database datble
            cur.executemany('INSERT INTO bar_sales (drinkName, category, priceDkk, unitsSold) VALUES (?, ?, ?, ?)', rows)

    print(f'Database created and populated at {db_path}')

# Get list of all sales data
def get_all():
    sales = []

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM bar_sales')

        # Get column names from cursor description
        columns = [column[0] for column in cur.description]

        # Fetch all rows and map each row to a column
        for row in cur.fetchall():
            sales.append(dict(zip(columns, row)))

    return sales
