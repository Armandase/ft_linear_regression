import pandas as pd
import argparse

header1 = "theta0"
header2 = "theta1"

def predict_value(theta0, theta1, value):
    prediction = theta0 + theta1 * value
    return prediction

def main(theta_path: str):
    theta0, theta1 = 0, 0
    try:
        data = pd.read_csv(theta_path)
        theta0 = data[header1][0]
        theta1 = data[header2][0]
    except Exception as e:
        print("Error to load", str(e))
        print("Theta0 & theta1 wille be equal to 0")
    print("Please enter a mileage:")
    input_string = input()
    if input_string.isdigit() == False or int(input_string) < 0:
        print("Wrong input, it must be a positive interger")
        return 1
    predicted = predict_value(theta0, theta1, int(input_string))
    print("Predicted value for", input_string, "km is", predicted, "$")
    if predicted < 0:
        print("The predicted value is negative, conceptually impossible to sell a car for a negative price but it follow the model slope")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--theta_path", help="theta path file", type=str, required=False, default="")
    
    args = parser.parse_args()
    main(theta_path=args.theta_path)
