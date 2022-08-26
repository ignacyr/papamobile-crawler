import requests
import pandas as pd
from datetime import datetime, date, timedelta
import os, json

if __name__ == "__main__":
    #all = requests.get("http://34.141.144.103:8000/base/").json()
    #all_df = pd.DataFrame.from_dict(all)
    
    yesterday = date.today() - timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%dT00:00:00Z")
    
    #yest_cars_df = all_df[all_df["added"] == yesterday]
    
    token = os.environ["PapiToken"]

    headers = {'Accept': 'application/json', "Authorization": f"Token {token}"}

    yest_cars = requests.get(f"http://34.141.144.103:8000/base/date_list?date={yesterday}", headers=headers).json()
    yest_cars_df = pd.DataFrame.from_dict(yest_cars)
    
    avg_price = round(yest_cars_df["price"].median())

    for fuel in ['Petrol', 'Diesel', 'Electric', 'Hybrid']:
        response = requests.get(f"http://34.141.144.103:8000/base/user_search?field=fuel&search=" + fuel, headers=headers).json()['median']
        requests.patch("http://34.141.144.103:8000/base/user_search/plots?search=" + fuel, data={"_" + fuel: response}, headers=headers)
        ### UPDATE fuel with response ###

    for mileage in range(1, 30):
        response = requests.get(f"http://34.141.144.103:8000/base/user_search?field=milage&search=" + str(mileage * 10), headers=headers).json()['median']
        data = r"{'_" + str(mileage * 10) + r"': " + str(int(response)) + r"}"
        data = data.replace("\'", "\"")
        update = requests.patch("http://34.141.144.103:8000/base/user_search/plots?search=" + str(mileage * 10), data=json.loads(data), headers=headers)
        ### UPDATE mileage with response ###

    for color in ['White', 'Gray', 'Black', 'Red', 'Other', 'Blue', 'Silver']:
        response = requests.get(f"http://34.141.144.103:8000/base/user_search?field=color&search=" + color, headers=headers).json()['median']
        update = requests.patch("http://34.141.144.103:8000/base/user_search/plots?search=" + color, data={"_" + color: int(response)}, headers=headers)
        ### UPDATE colors with response ###

    resp_avg = requests.post("http://34.141.144.103:8000/base/daily_avg", data={"date": yesterday, "price": avg_price, "count": len(yest_cars_df)}, headers=headers)
    print(resp_avg.json())

    
