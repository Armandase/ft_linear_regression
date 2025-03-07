import numpy as np
from matplotlib import pyplot as plt
import csv

def normalize_data(array):
    frobenius_norm = np.linalg.norm(array)
    normalized_array = array / frobenius_norm
    return normalized_array, frobenius_norm

def plot_data(data, header1, header2, predict):
    plt.scatter(data[header1], data[header2])
    plt.xlabel(header1)
    plt.ylabel(header2)
    plt.plot(data[header1], predict, c='red')
    plt.show()

def precision(theta0, theta1, x, y_waited):
    sum_diff = sum((y_waited - (theta1 * x + theta0)) ** 2)
    sum_mean = sum((y_waited - y_waited.mean()) ** 2)
    computed_precision = 1 - sum_diff / sum_mean
    computed_precision *= 100
    return computed_precision

def write_theta(theta0, theta1):
    try :
        f = open('theta.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(["theta0", "theta1"])
        writer.writerow([theta0, theta1])
        f.close()
    except Exception as e:
        print("Error to write", str(e))
        exit(1)

def ols_computation(X, Y):
    X = np.array(X)
    Y = np.array(Y)
    X_mean = np.mean(X)
    Y_mean = np.mean(Y)
    XY_mean = np.mean(X * Y)
    X_squared_mean = np.mean(np.square(X))
    
    alpha = (XY_mean - X_mean * Y_mean) / (X_squared_mean - np.square(X_mean))

    beta = Y_mean - alpha * np.mean(X)
    precis = precision(beta, alpha, X, Y)
    print("The precision with OLS(moindre carré ordinaire) is", '%.4f'%precis, "%")

