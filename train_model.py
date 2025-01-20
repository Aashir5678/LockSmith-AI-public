
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import pickle
import numpy as np
import pandas as pd

# Uses the following data set for training: https://www.kaggle.com/datasets/bhavikbb/password-strength-classifier-dataset/data\
# 0 - weak password, 1 - medium password, 2 - strong password
DATA_SIZE = 10000


def password_features(password):
    length = len(password)
    lowercase_count = 0
    uppercase_count = 0
    digits = 0
    special_chars = 0

    for char in password:
        if char.islower():
            lowercase_count += 1
        
        elif char.isupper():
            uppercase_count += 1

        elif char.isdigit():
            digits += 1

        elif char.isalnum():
            special_chars += 1

    return np.array([length, lowercase_count, uppercase_count, digits, special_chars])


def train_model(file="training/data.csv"):
    data = pd.read_csv(file, on_bad_lines='skip')

    data_encoder = OneHotEncoder(handle_unknown='ignore') # Need to encode password strings to fit them
    data_list = []

    passwords = data["password"].values[:DATA_SIZE]
    passwords_list = list(passwords)

    password_strength = data["strength"].values[:DATA_SIZE]

    password_data = data_encoder.fit_transform(passwords.reshape(-1, 1))
    password_info = []

    for password in passwords_list:
        password_info.append(password_features(password))

    password_data = np.array(password_info)

    x_train, x_test, y_train, y_test = train_test_split(password_data, password_strength, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, class_weight="balanced")
    model.fit(x_train, y_train)

    return model, x_test, y_test


def save_model(model, file="training/model.pickle"):
    with open(file, "wb") as f:
        pickle.dump(model, f)

def get_model(file="training/model.pickle"):
    with open(file, "rb") as f:
        model = pickle.load(f)

    return model



if __name__ == "__main__":
    model, x_test, y_test = train_model()
    print (model.score(x_test, y_test))
    save_model(model)


    import matplotlib.pyplot as plt

    # Predict on test data
    y_pred = model.predict(x_test)

    # Scatter plot of actual vs predicted values
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.6, color='blue', label='Predicted vs Actual')
    plt.plot([0, 2], [0, 2], color='red', linestyle='--', label='Perfect Prediction (y=x)')
    plt.xlabel('Actual Password Strength')
    plt.ylabel('Predicted Password Strength')
    plt.title('Actual vs Predicted Password Strength')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot residuals
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.6, color='purple', label='Residuals')
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel('Predicted Password Strength')
    plt.ylabel('Residuals (Actual - Predicted)')
    plt.title('Residuals of Password Strength Predictions')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Optional: Histogram of predictions
    plt.figure(figsize=(10, 6))
    plt.hist(y_test, bins=20, alpha=0.5, color='green', label='Actual Strengths')
    plt.hist(y_pred, bins=20, alpha=0.5, color='blue', label='Predicted Strengths')
    plt.xlabel('Password Strength')
    plt.ylabel('Frequency')
    plt.title('Distribution of Actual vs Predicted Password Strength')
    plt.legend()
    plt.show()