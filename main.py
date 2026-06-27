import pandas as pd
import sqlite3

df = pd.read_csv("superstore.csv", encoding="latin-1")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df["order_date"] = pd.to_datetime(df["order_date"])

conn = sqlite3.connect("sales.db")
df.to_sql("orders", conn, if_exists='replace', index=False)

def run_query(query):
    return pd.read_sql_query(query, conn)

def sales_by_region():
    return run_query("""
        SELECT region, SUM(sales) as total_sales
        FROM orders
        GROUP BY region
        ORDER BY total_sales DESC
    """)

def bottom_5_products():
    return run_query("""
        SELECT product_name, SUM(sales) as total_sales
        FROM orders
        GROUP BY product_name
        ORDER BY total_sales ASC
        LIMIT 5
    """)

def top_3_discounted():
    return run_query("""
        SELECT `sub-category`, AVG(discount) as avg_discount
        FROM orders
        GROUP BY `sub-category`
        ORDER BY avg_discount DESC
        LIMIT 3
    """)

def sales_profit_by_year():
    return run_query("""
        SELECT strftime('%Y', order_date) as year,
               SUM(sales) as total_sales,
               SUM(profit) as total_profit
        FROM orders
        GROUP BY year
        ORDER BY year
    """)

def ship_mode_usage():
    return run_query("""
        SELECT ship_mode, COUNT(ship_mode) as total_orders
        FROM orders
        GROUP BY ship_mode
        ORDER BY total_orders DESC
    """)

def top_5_customers():
    return run_query("""
        SELECT customer_id, customer_name,
               SUM(sales) as total_purchases
        FROM orders
        GROUP BY customer_id, customer_name
        ORDER BY total_purchases DESC
        LIMIT 5
    """)

def avg_order_by_category():
    return run_query("""
        SELECT category, AVG(sales) as average_order_value
        FROM orders
        GROUP BY category
        ORDER BY average_order_value DESC
    """)

def negative_profit_states():
    return run_query("""
        SELECT state, SUM(profit) as net_profit
        FROM orders
        GROUP BY state
        HAVING SUM(profit) < 0
        ORDER BY net_profit ASC
    """)

def monthly_profit_2017():
    return run_query("""
        SELECT strftime('%m', order_date) as month,
               SUM(profit) as monthly_profit
        FROM orders
        WHERE strftime('%Y', order_date) = '2017'
        GROUP BY month
        ORDER BY month
    """)

def top_segment():
    return run_query("""
        SELECT segment, SUM(sales) as total_revenue
        FROM orders
        GROUP BY segment
        ORDER BY total_revenue DESC
        LIMIT 1
    """)

def menu():
    print("\n===== Sales Analyzer =====")
    print("1.  Sales by Region")
    print("2.  Bottom 5 Products")
    print("3.  Top 3 Discounted Sub-Categories")
    print("4.  Sales and Profit by Year")
    print("5.  Ship Mode Usage")
    print("6.  Top 5 Customers")
    print("7.  Average Order Value by Category")
    print("8.  States with Negative Profit")
    print("9.  Monthly Profit Trend 2017")
    print("10. Top Segment by Revenue")
    print("0.  Exit")
    return input("\nEnter choice: ")

while True:
    choice = menu()
    if choice == "1":
        print(sales_by_region())
    elif choice == "2":
        print(bottom_5_products())
    elif choice == "3":
        print(top_3_discounted())
    elif choice == "4":
        print(sales_profit_by_year())
    elif choice == "5":
        print(ship_mode_usage())
    elif choice == "6":
        print(top_5_customers())
    elif choice == "7":
        print(avg_order_by_category())
    elif choice == "8":
        print(negative_profit_states())
    elif choice == "9":
        print(monthly_profit_2017())
    elif choice == "10":
        print(top_segment())
    elif choice == "0":
        print("Goodbye!")
        conn.close()
        break
    else:
        print("Invalid choice. Enter 0-10.")