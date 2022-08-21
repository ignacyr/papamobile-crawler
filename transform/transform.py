import requests
import pandas as pd
from datetime import datetime, date, timedelta
import os

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
    
    resp_avg = requests.post("http://34.141.144.103:8000/base/daily_avg", data={"date": yesterday, "price": avg_price, "count": len(yest_cars_df)}, headers=headers)
    print(resp_avg.json())

    
