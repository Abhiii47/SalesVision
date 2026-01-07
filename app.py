from flask import Flask, jsonify, render_template
import sqlite3
import os
import random
import datetime

app = Flask(__name__)
DB_PATH = 'sales.db'

def get_db_connection():
    # check_same_thread=False is often needed for serverless if using SQLite, 
    # though it's read-only mostly.
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    conn = get_db_connection()
    data = {}
    
    try:
        # 1. Total revenue and profit
        row = conn.execute('SELECT SUM(Sales) AS total_revenue, SUM(Profit) AS total_profit FROM sales_data').fetchone()
        data['total_metrics'] = dict(row) if row else {}

        # 2. Revenue by region
        rows = conn.execute('SELECT Region, SUM(Sales) AS revenue FROM sales_data GROUP BY Region ORDER BY revenue DESC').fetchall()
        data['revenue_by_region'] = [dict(row) for row in rows]

        # 3. Top 10 customers by revenue
        rows = conn.execute('SELECT Customer_Name, SUM(Sales) AS total_spent FROM sales_data GROUP BY Customer_Name ORDER BY total_spent DESC LIMIT 10').fetchall()
        data['top_customers'] = [dict(row) for row in rows]

        # 4. Profitability by category
        rows = conn.execute('SELECT Category, SUM(Profit) AS profit FROM sales_data GROUP BY Category ORDER BY profit DESC').fetchall()
        data['profit_by_category'] = [dict(row) for row in rows]

        # 5. Orders with negative profit (loss-making)
        rows = conn.execute('SELECT Order_ID, Sales, Profit FROM sales_data WHERE Profit < 0 LIMIT 10').fetchall()
        data['negative_profit_orders'] = [dict(row) for row in rows]

        # 6. Average order value
        row = conn.execute('SELECT AVG(Sales) AS avg_order_value FROM sales_data').fetchone()
        data['avg_order_value'] = dict(row)['avg_order_value'] if row else 0

    except Exception as e:
        print(f"Error querying database: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify(data)

@app.route('/api/activity')
def get_activity():
    # Serverless-friendly: Generate random activity on the fly
    users = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank']
    actions = ['New Order', 'Payment Received', 'Refund Processed', 'New User Signup', 'Order Shipped']
    
    activity_data = []
    now = datetime.datetime.now()
    
    # Generate 10 recent mock events
    for i in range(10):
        # Slightly offset times to look like a history
        timestamp = (now - datetime.timedelta(seconds=i*5 + random.randint(1,4))).strftime("%Y-%m-%d %H:%M:%S")
        user = random.choice(users)
        action = random.choice(actions)
        
        if action in ['New Order', 'Payment Received', 'Refund Processed']:
            amount = round(random.uniform(10.0, 500.0), 2)
            if action == 'Refund Processed':
                amount = -amount
        else:
            amount = 0.00
            
        activity_data.append({
            'timestamp': timestamp,
            'user': user,
            'action': action,
            'amount': amount
        })
    
    return jsonify(activity_data) # Returns 10 items. Frontend handles polling.

if __name__ == '__main__':
    app.run(debug=True, port=5000)
