import requests
import pandas as pd
from datetime import datetime, date, timedelta

if __name__ == "__main__":
    all = requests.get("http://34.141.144.103:8000/base/").json()
    all_df = pd.DataFrame.from_dict(all)
    
    yesterday = date.today() - timedelta(days=1)
    yesterday = yesterday.strftime("%Y-%m-%dT00:00:00Z")
    yesterday = "2022-08-15T00:00:00Z"
    avg_price = round(all_df[all_df["added"] == yesterday]["price"].median())
    
    resp_avg = requests.post("http://34.141.144.103:8000/base/daily_avg", {"date": yesterday, "price": avg_price})
    print(resp_avg.json())

