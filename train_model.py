import pandas as pd
import numpy as np
import argparse
from utils import normalize_data, plot_data, precision, write_theta

def train_theta(data, norm_x, norm_y, iteration=1000, learning_rate=0.5, early_stop=0.0000001):
    theta0, theta1 = 0, 0
    sum0, sum1 = 0, 0
    m = data.shape[0]
    
    old_t0, old_t1 = 0, 0
    diff = np.inf
    for _ in range(iteration):
        sum0, sum1 = 0, 0
        for value in data:
            sum0 += (theta0 + theta1 * value[0]) - value[1]
            sum1 += ((theta0 + theta1 * value[0]) - value[1]) * value[0]
        theta0 -= (learning_rate * (1/m) * sum0)
        theta1 -= (learning_rate * (1/m) * sum1)

        diff = abs((old_t0 - theta0) + (old_t1 - theta1))
        if diff < early_stop:
            break
        old_t0 = theta0
        old_t1 = theta1
    
    theta0 = theta0 * norm_y
    theta1 = theta1 * (norm_y / norm_x)
    return theta0, theta1

def main(data_path: str, learning_rate: float, iteration: int, early_stop: float):
    try:
        data = pd.read_csv(data_path)
    except Exception as e:
        print("Error to load", str(e))
        return 1
    if len(data.columns) != 2:
        print("Wrong number of columns")
        return 1
    
    header1, header2 = data.columns.values.tolist()

    data_noramlized = data.copy()
    data_noramlized[header1], norm_x = normalize_data(data[header1])
    data_noramlized[header2], norm_y = normalize_data(data[header2])

    theta0, theta1 = train_theta(np.array(data_noramlized), norm_x, norm_y, iteration, learning_rate, early_stop)
    write_theta(theta0, theta1)
    predict = data[header1] * theta1 + theta0
    plot_data(data, header1, header2, predict)
    precision(theta0, theta1, data[header1], data[header2])
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_path", help="data path file", type=str, required=True)
    parser.add_argument("--learning_rate", "-lr", help="the learning speed ", type=float, default=0.5)
    parser.add_argument("--iteration", "-i", help="the number of iteration for the training", type=int, default=1000)
    parser.add_argument("--early_stop", "-e", help="Use this to stop the training if the difference between two iterations exceeds early_stop", type=float, default=0.0000001)

    args = parser.parse_args()
    main(data_path=args.data_path, learning_rate=args.learning_rate, iteration=args.iteration, early_stop=args.early_stop)
