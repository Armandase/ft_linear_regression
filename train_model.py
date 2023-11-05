import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import csv

learning_rate = 0.5
iteration = 1000
valid = 0.0000001

def train_theta(data, norm_x, norm_y):
    theta0, theta1 = 0, 0
    sum0, sum1 = 0, 0
    m = data.shape[0]
    
    old_t0, old_t1 = 0, 0
    diff = 10.0
    while diff > valid:
        sum0, sum1 = 0, 0
        for value in data:
            sum0 += (theta0 + theta1 * value[0]) - value[1]
            sum1 += ((theta0 + theta1 * value[0]) - value[1]) * value[0]
        old_t0 = theta0
        old_t1 = theta1
        theta0 -= learning_rate * (1/m) * sum0
        theta1 -= learning_rate * (1/m) * sum1
        diff = abs((old_t0 - theta0) + (old_t1 - theta1))
    
    theta0 = theta0 * norm_y
    theta1 = theta1 * (norm_y / norm_x)
    return theta0, theta1

def normalize_data(array):
    frobenius_norm = np.linalg.norm(array)
    normalized_array = array / frobenius_norm
    return normalized_array, frobenius_norm

def plot_data(data, header1, header2, predict):
    plt.scatter(data[header1], data[header2])
    plt.xlabel(data.columns[0])
    plt.ylabel(data.columns[1])
    plt.plot(data[header1], predict, c='red')
    plt.show()

def precision(theta0, theta1, x, y_waited):
    sum_diff = sum((y_waited - (theta1 * x + theta0)) ** 2)
    sum_mean = sum((y_waited - y_waited.mean()) ** 2)
    computed_precision = 1 - sum_diff / sum_mean
    print("The precision is", '%.4f'%computed_precision, "%")

def write_theta(theta0, theta1):
    f = open('theta.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(["theta0", "theta1"])
    writer.writerow([theta0, theta1])
    f.close()


def main():
    if len(sys.argv) != 2:
        print("Wrong number of arguments")
        return 1
    try:
        data = pd.read_csv(sys.argv[1])
    except :
        print("Error to load", sys.argv[1])
        return 1
    if len(data.columns) != 2:
        print("Wrong number of columns")
        return 1
    
    header1, header2 = data.columns[0], data.columns[1]
    data_noramlized = data.copy()
    data_noramlized[header1], norm_x = normalize_data(data[header1])
    data_noramlized[header2], norm_y = normalize_data(data[header2])

    theta0, theta1 = train_theta(np.array(data_noramlized), norm_x, norm_y)
    write_theta(theta0, theta1)
    x_computed = data[header1] * theta1 + theta0
    plot_data(data, header1, header2, x_computed)
    precision(theta0, theta1, data[header1], data[header2])
    

if __name__ == "__main__":
    main()
