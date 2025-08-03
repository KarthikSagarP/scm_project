# 📦 SCM Demand Prediction Using LSTM

This is a Python-based Supply Chain Management (SCM) project that processes historical product usage data and predicts future demand using an LSTM (Long Short-Term Memory) model. It includes a GUI for ease of use and connects to a MySQL database.

---

## 🧠 How It Works

1. Load data from an Excel file and/or MySQL database.
2. Preprocess and scale the data using a saved MinMaxScaler.
3. Feed the data into a trained LSTM model (`supply_demand_lstm.h5`) to predict future demand.
4. Show the results using a simple `tkinter` GUI.

---

## 🛠 Tech Stack

- Python
- LSTM using TensorFlow/Keras
- Data Processing: pandas, NumPy, scikit-learn
- GUI: tkinter
- Database: MySQL (via `mysql-connector-python`)

---

## 🚀 How to Run

1. **Install the required packages**
   ```bash
   pip install -r requirements.txt
