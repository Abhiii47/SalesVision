import sqlite3
import random
import datetime

def create_connection():
    conn = sqlite3.connect('sales.db')
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales_data (
            Order_ID TEXT PRIMARY KEY,
            Order_Date TEXT,
            Customer_Name TEXT,
            Region TEXT,
            Category TEXT,
            Sales REAL,
            Profit REAL
        )
    ''')
    conn.commit()

def generate_data(conn, num_rows=200):
    cursor = conn.cursor()
    
    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = ['Technology', 'Furniture', 'Office Supplies', 'Automotive', 'Fashion']
    first_names = ['John', 'Jane', 'Michael', 'Emily', 'David', 'Sarah', 'Chris', 'Amanda', 'James', 'Laura']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson']
    
    data = []
    
    for _ in range(num_rows):
        order_id = f"ORD-{random.randint(10000, 99999)}"
        
        # Random date within last year
        start_date = datetime.date.today() - datetime.timedelta(days=365)
        random_days = random.randint(0, 365)
        order_date = (start_date + datetime.timedelta(days=random_days)).isoformat()
        
        customer_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        region = random.choice(regions)
        category = random.choice(categories)
        
        # Sales between 10.00 and 1000.00
        sales = round(random.uniform(10.0, 1000.0), 2)
        
        # Profit margin between -20% and 40%
        profit_margin = random.uniform(-0.2, 0.4)
        profit = round(sales * profit_margin, 2)
        
        data.append((order_id, order_date, customer_name, region, category, sales, profit))
        
    cursor.executemany('''
        INSERT OR IGNORE INTO sales_data (Order_ID, Order_Date, Customer_Name, Region, Category, Sales, Profit)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)
    
    conn.commit()
    print(f"Successfully inserted {num_rows} rows into sales_data.")

def main():
    conn = create_connection()
    create_table(conn)
    generate_data(conn)
    conn.close()

if __name__ == '__main__':
    main()
