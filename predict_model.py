import pandas as pd
import sys

header1 = "theta0"
header2 = "theta1"

def predict_value(theta0, theta1, value):
    prediction = theta0 + theta1 * value
    return prediction

def main():
    theta0, theta1 = 0, 0
    try:
        data = pd.read_csv("./theta.csv")
        theta0 = data[header1][0]
        theta1 = data[header2][0]
    except :
        print("Error to load theta.csv")
        print("Theta0 & theta1 wille be equal to 0")
    print("Please enter a mileage:")
    input_string = input()
    if input_string.isdigit() == False or int(input_string) < 0:
        print("Wrong input, it must be a positive interger number")
        return 1
    predicted = predict_value(theta0, theta1, int(input_string))
    print("Value predict for", input_string, "is", predicted)
    
if __name__ == "__main__":
    main()
