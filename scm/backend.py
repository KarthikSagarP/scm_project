import pandas as pd
import mysql.connector

# Read Excel file
df = pd.read_excel("Online Retail.xlsx")

# Drop missing values
df = df.dropna()

# Convert InvoiceDate to proper datetime format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
df = df.dropna(subset=['InvoiceDate'])  # Remove rows where InvoiceDate couldn't be converted

# Ensure correct column order
df = df[['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']]

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="C@pshe!1",
    database="scm"
)
cursor = conn.cursor()

# Create Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        InvoiceNo VARCHAR(20),
        StockCode VARCHAR(20),
        Description TEXT,
        Quantity INT,
        InvoiceDate DATETIME,
        UnitPrice DECIMAL(10,2),
        CustomerID INT,
        Country VARCHAR(50)
    )
''')

# Insert Data
for _, row in df.iterrows():
    cursor.execute('''
    INSERT INTO sales (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
''', (
    row['InvoiceNo'], 
    row['StockCode'], 
    row['Description'], 
    row['Quantity'], 
    row['InvoiceDate'].strftime('%Y-%m-%d %H:%M:%S'),  # Convert to MySQL DATETIME format
    row['UnitPrice'], 
    row['CustomerID'], 
    row['Country']
))


print("Excel data uploaded to MySQL successfully!")

conn.commit()
cursor.close()
conn.close()
