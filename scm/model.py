import pandas as pd
import numpy as np
import mysql.connector
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="C@pshe!1",
    database="scm"
)
cursor = conn.cursor()

# Fetch sales data
query = "SELECT InvoiceDate, Quantity FROM sales ORDER BY InvoiceDate"
df = pd.read_sql(query, conn)
cursor.close()
conn.close()

# Convert date column to datetime and set as index
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df.set_index('InvoiceDate', inplace=True)

# Resample data to daily sales
df = df.resample('D').sum()

# Normalize data
scaler = MinMaxScaler()
df_scaled = scaler.fit_transform(df)

# Create sequences for LSTM
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])
    return np.array(X), np.array(y)

seq_length = 30  # Using past 30 days to predict next day
X, y = create_sequences(df_scaled, seq_length)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

# Build LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(seq_length, 1)),
    Dropout(0.2),
    LSTM(50, return_sequences=False),
    Dropout(0.2),
    Dense(25, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# Train model
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test), verbose=1)

# Save model
model.save("supply_demand_lstm.h5")

print("Model training complete and saved!")
