import joblib
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from model import X_train

# Load your training data (replace this with your actual data)
# X_train = np.load("X_train.npy")  # Example way of loading it

# Reshape X_train to 2D: (samples, features)
X_train_reshaped = X_train.reshape(X_train.shape[0], -1)

# Initialize and fit scaler
scaler = MinMaxScaler()
scaler.fit(X_train_reshaped)

# Save the scaler
joblib.dump(scaler, "scaler.pkl")
print("Scaler saved successfully!")
