import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# -------------------------
# Load Dataset
# -------------------------
df = pd.read_csv("Sample.csv", encoding="latin1")

# -------------------------
# Data Cleaning
# -------------------------
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Remove missing values
df = df.dropna()

# -------------------------
# Time-Based Feature Engineering
# -------------------------
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month
df['Day'] = df['Order Date'].dt.day
df['DayOfWeek'] = df['Order Date'].dt.dayofweek

# -------------------------
# Aggregate Daily Sales
# -------------------------
daily_sales = df.groupby('Order Date')['Sales'].sum().reset_index()

# Create numerical time feature
daily_sales['Day_Number'] = range(len(daily_sales))

# -------------------------
# Prepare Data
# -------------------------
X = daily_sales[['Day_Number']]
y = daily_sales['Sales']

# -------------------------
# Train Model
# -------------------------
model = LinearRegression()
model.fit(X, y)

# -------------------------
# Predictions
# -------------------------
daily_sales['Predicted_Sales'] = model.predict(X)

# -------------------------
# Error Analysis
# -------------------------
mae = mean_absolute_error(
    daily_sales['Sales'],
    daily_sales['Predicted_Sales']
)

print("\nMean Absolute Error:")
print(mae)

# -------------------------
# Future Forecast
# -------------------------
future_days = pd.DataFrame({
    'Day_Number': [len(daily_sales) + i for i in range(1, 31)]
})

future_predictions = model.predict(future_days)

print("\nNext 30 Days Forecast")

for i, value in enumerate(future_predictions, start=1):
    print(f"Day {i}: {value:.2f}")

# -------------------------
# Visualization
# -------------------------
plt.figure(figsize=(12,6))

plt.plot(
    daily_sales['Order Date'],
    daily_sales['Sales'],
    label='Actual Sales'
)

plt.plot(
    daily_sales['Order Date'],
    daily_sales['Predicted_Sales'],
    label='Predicted Sales'
)

plt.title("Sales Forecast")
plt.xlabel("Date")
plt.ylabel("Sales")
plt.legend()

plt.savefig("forecast.png")

plt.show()