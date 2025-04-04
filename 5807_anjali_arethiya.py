# -*- coding: utf-8 -*-
"""5807_Anjali_Arethiya

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xDb0YphTBJ8tdDQFC4LYhvarcVMNDjVw
"""

# Import Libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import r2_score, accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

from google.colab import drive
drive.mount('/content/drive')

# Step 2: Download Dataset
data = '/content/drive/MyDrive/cardekho_dataset.csv'
df = pd.read_csv(data)

# 2. the problem is regression
print("Target Variable: selling_price")
print(df.head())

print(df.tail())

# 3. Analyze Target Variable
print("Target Variable Description:")
print(df['selling_price'].describe())

plt.figure(figsize=(10, 6))
sns.histplot(df['selling_price'], kde=True)
plt.title('Distribution of Selling Price')
plt.xlabel('Selling Price')
plt.show()

# 4. Check and Remove Duplicates
duplicates = df.duplicated()
print(f"Number of Duplicate Rows: {duplicates.sum()}")
df = df.drop_duplicates()
print("Duplicates Removed")

# 5. Check Data Inconsistency
print("Data Types Information:")
df.info()

for col in df.columns:
    if df[col].apply(type).nunique() > 1:
        print(f"Inconsistent datatypes in column: {col}")

# Check Missing Values
print("Missing Values Count:")
print(df.isna().sum())

# Separate Numeric and Non-Numeric Columns
numeric_cols = df.select_dtypes(include=['number']).columns
non_numeric_cols = df.select_dtypes(exclude=['number']).columns

# Fill Missing Values in Numeric Columns with Median
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Fill Missing Values in Non-Numeric Columns with Mode
for col in non_numeric_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

print("Missing Values Treated")
print(df.isna().sum())

# 7. Exploratory Data Analysis (EDA)
print(df.describe())

# Scatter Plot
sns.scatterplot(x='mileage', y='selling_price', data=df)
plt.title('Feature vs Selling Price')
plt.show()

# Boxplot
sns.boxplot(x=df['selling_price'])
plt.title('Boxplot of Selling Price')
plt.show()

# Distribution Plot
sns.distplot(df['selling_price'], kde=True)
plt.title('Distribution Plot of Selling Price')
plt.show()

# Countplot (categorical column)
sns.countplot(x=df['fuel_type'])
plt.title('Countplot for Fuel Type')
plt.show()

# 8. Scaling (Standardization)
scaler = StandardScaler()
numerical_features = df.select_dtypes(include=['int64', 'float64']).columns
df[numerical_features] = scaler.fit_transform(df[numerical_features])
print("Scaling Applied")

# 9. Encoding (Convert categorical variables to numerical)
df = pd.get_dummies(df, drop_first=True)
print("Encoding Completed")

# 10. Split Data into Train and Test
X = df.drop(columns=['selling_price'])
y = df['selling_price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data Split into Train and Test")

# 11. Apply Machine Learning Models
# Decision Tree
dt_model = DecisionTreeRegressor()
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)
dt_accuracy = r2_score(y_test, dt_pred)
print(f"Decision Tree R² Score: {dt_accuracy}")

# Random Forest
rf_model = RandomForestRegressor()
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_accuracy = r2_score(y_test, rf_pred)
print(f"Random Forest R² Score: {rf_accuracy}")

# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)
lr_accuracy = r2_score(y_test, lr_pred)
print(f"Linear Regression R² Score: {lr_accuracy}")

result=pd.DataFrame({"Actual":y_test,"Predicted":lr_pred})
result.head(10)

# Logistic Regression (for a classification task)
y_class = (y > y.median()).astype(int)
X_train_class, X_test_class, y_train_class, y_test_class = train_test_split(X, y_class, test_size=0.2, random_state=42)

log_reg_model = LogisticRegression(max_iter=500)
log_reg_model.fit(X_train_class, y_train_class)
log_reg_pred = log_reg_model.predict(X_test_class)
log_reg_accuracy = accuracy_score(y_test_class, log_reg_pred)
print(f"Logistic Regression Accuracy: {log_reg_accuracy}")

# Feedforward Neural Network (FNN)
fnn_model = Sequential([
    Dense(64, activation='relu', input_dim=X_train.shape[1]),
    Dense(32, activation='relu'),
    Dense(1)
])

fnn_model.compile(optimizer=Adam(learning_rate=0.01), loss='mse', metrics=['mae'])
fnn_model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1, validation_split=0.2)

fnn_pred = fnn_model.predict(X_test).flatten()
fnn_accuracy = r2_score(y_test, fnn_pred)
print(f"FNN R² Score: {fnn_accuracy}")

# 12. Compare Model Accuracies
print("\nModel Comparison:")
print(f"Decision Tree: {dt_accuracy:.2f}")
print(f"Random Forest: {rf_accuracy:.2f}")
print(f"Linear Regression: {lr_accuracy:.2f}")
print(f"Logistic Regression (Classification): {log_reg_accuracy:.2f}")
print(f"Feedforward Neural Network: {fnn_accuracy:.2f}")

# Target Accuracy Check
if max(dt_accuracy, rf_accuracy, lr_accuracy, fnn_accuracy) > 0.8:
    print("Target accuracy of >80% achieved")
else:
    print("Target accuracy not achieved. Consider further tuning or advanced models.")