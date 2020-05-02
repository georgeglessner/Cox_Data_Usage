#!/usr/bin/python3

from config import USERNAME, PASSWORD
import requests

login_url = "https://idm.east.cox.net/idm/coxnetlogin"
data_url = "https://www.cox.com/internet/mydatausage.cox"
stats_url = "https://www.cox.com/internet/ajaxDataUsageJSON.ajax"

cox_user = USERNAME
cox_pass = PASSWORD

with requests.Session() as session:
    payload = {
        "onsuccess": "https%3A%2F%2Fwww.cox.com%2Fresimyaccount%2Fhome.html",
        "targetFN": "COX.net",
        "emaildomain": "@cox.net",
        "username": USERNAME,
        "password": PASSWORD,
        "rememberme": "on",
    }

    headers = {
        "Host": "www.cox.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    login = session.post(login_url, data=payload)
    session.get("https://www.cox.com/internet/mydatausage.cox", headers=headers)
    data = session.get(stats_url, headers=headers)

json_dump = data.json()

percentage = json_dump["modemDetails"][0]["dataUsed"]["renderPercentage"]
current_used = int(
    json_dump["modemDetails"][0]["dataUsed"]["totalDataUsed"].replace("&#160;GB", "")
)
total_plan = int(json_dump["modemDetails"][0]["dataPlan"].replace("&#160;GB", ""))
billing_period = json_dump["modemDetails"][0]["servicePeriod"]

print("\nData usage for {}".format(billing_period))
print("Used: {} GB".format(current_used))
print("Remaining: {} GB".format(total_plan - current_used))
print("Percentage Used: {}%\n".format(percentage))
