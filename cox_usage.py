#!/usr/bin/python
# cox_usage.py
# Script designed to get Cox Communications internet usage
#
# Version 1.0
# Original Author : Rick Rocklin
# Original Date   : 10/02/2017
#
# 10/17/2017: Output to file
# 11/02/2017: Updated to use mechanicalsoup
from config import USERNAME, PASSWORD
import mechanicalsoup
import re
import json
import os

# URL that we authenticate against
login_url = "https://www.cox.com/resaccount/sign-in.cox"
# URL that we grab all the data from
stats_url = "https://www.cox.com/internet/mydatausage.cox"
# Your cox user account (e.g. username@cox.net) and password
cox_user = USERNAME
cox_pass = PASSWORD

# Setup browser
browser = mechanicalsoup.StatefulBrowser(
    soup_config={"features": "lxml"},
    user_agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13",
)

# Open the login URL
login_page = browser.get(login_url)

# Similar to assert login_page.ok but with full status code in case of failure.
login_page.raise_for_status()

# Find the form named sign-in
login_form = mechanicalsoup.Form(login_page.soup.select_one('form[name="sign-in"]'))

# Specify username and password
login_form.input({"username": cox_user, "password": cox_pass})

# Submit the form
browser.submit(login_form, login_page.url)

# Read the stats URL
stats_page = browser.get(stats_url)

# Grab the script with the stats in it
stats = stats_page.soup.findAll("script", string=re.compile("utag_data"))[0].string

# Split and RSplit on the first { and on the last } which is where the data object is located
jsonValue = "{%s}" % (stats.split("{", 1)[1].rsplit("}", 1)[0],)

# Load into json
data = json.loads(jsonValue)

print(f"\nTotal Used: {data['dumUsage']} GB")
print(f"Total Left: {int(data['dumLimit']) - int(data['dumUsage'])} GB")
print(f"Days Left: {data['dumDaysLeft']}\n")
