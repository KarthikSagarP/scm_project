import pandas as pd
import mysql.connector
import tkinter as tk
from tkinter import messagebox
import joblib
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError

# Load the trained LSTM model and scaler
model = load_model("supply_demand_lstm.h5", custom_objects={"mse": MeanSquaredError()})
scaler = joblib.load("scaler.pkl")

# GUI Setup
root = tk.Tk()
root.title("Supply-Demand Forecasting")

def predict_demand():
    try:
        stock_code = stock_entry.get()
        quantity = float(quantity_entry.get())
        unit_price = float(price_entry.get())
        
        # Prepare input data
        input_data = np.array([[quantity, unit_price]])
        input_data_scaled = scaler.transform(input_data)
        input_data_scaled = np.reshape(input_data_scaled, (1, 1, input_data_scaled.shape[1]))  # Ensure correct shape for LSTM

        
        # Predict
        predicted_demand = model.predict(input_data_scaled)
        predicted_demand = scaler.inverse_transform(predicted_demand)
        
        messagebox.showinfo("Prediction Result", f"Predicted Demand: {predicted_demand[0][0]:.2f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Layout
tk.Label(root, text="Stock Code:").grid(row=0, column=0)
stock_entry = tk.Entry(root)
stock_entry.grid(row=0, column=1)

tk.Label(root, text="Quantity:").grid(row=1, column=0)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=1, column=1)

tk.Label(root, text="Unit Price:").grid(row=2, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=2, column=1)

tk.Button(root, text="Predict Demand", command=predict_demand).grid(row=3, column=0, columnspan=2)

root.mainloop()
