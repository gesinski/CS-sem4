import numpy as np
import matplotlib.pyplot as plt

from data import get_data, inspect_data, split_data

data = get_data()
inspect_data(data)

train_data, test_data = split_data(data)

# Simple Linear Regression
# predict MPG (y, dependent variable) using Weight (x, independent variable) using closed-form solution
# y = theta_0 + theta_1 * x - we want to find theta_0 and theta_1 parameters that minimize the prediction error

# We can calculate the error using MSE metric:
# MSE = SUM (from i=1 to n) (actual_output - predicted_output) ** 2

# get the columns
y_train = train_data['MPG'].to_numpy()
x_train = train_data['Weight'].to_numpy()

y_test = test_data['MPG'].to_numpy()
x_test = test_data['Weight'].to_numpy()

# calculate closed-form solution
theta_best = [0, 0]

X_train = np.c_[np.ones(x_train.shape[0]), x_train]  # add columns of ones
theta_best = np.linalg.inv(X_train.T @ X_train) @ X_train.T @ y_train 

# prediction values
X_test = np.c_[np.ones(x_test.shape[0]), x_test] 
y_test_prediction = X_test @ theta_best

# calculate error
mse = np.mean((y_test - y_test_prediction) ** 2)
print(f"Closed-form MSE: {mse}")

# plot the regression line
x = np.linspace(min(x_test), max(x_test), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()

# standardization
x_train_std = (x_train - np.mean(x_train)) / np.std(x_train)
X_train_std = np.c_[np.ones(x_train_std.shape[0]), x_train_std]

x_test_std = (x_test - np.mean(x_train)) / np.std(x_train)
X_test_std = np.c_[np.ones(x_test_std.shape[0]), x_test_std] 

# calculate theta using Batch Gradient Descent
theta_best = [0.0, 0.0]
iterations = 500
learning_rate = 0.01
for i in range(iterations):
    gradient = (X_train_std.T @ (X_train_std @ theta_best - y_train)) / len(X_train_std)
    theta_best -= learning_rate * gradient


# calculate error
mse2 = np.mean((y_test - X_test_std @ theta_best) ** 2)
print(f"Closed-form MSE2: {mse2}")

# plot the regression line
x = np.linspace(min(x_test_std), max(x_test_std), 100)
y = float(theta_best[0]) + float(theta_best[1]) * x
plt.plot(x, y)
plt.scatter(x_test_std, y_test)
plt.xlabel('Weight')
plt.ylabel('MPG')
plt.show()