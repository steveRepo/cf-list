##### CFLIST Version 1

# This script makes paginated API calls and outputs the list items to a single list in file: items.json

# To use make sure you have python installed and add you variables below
# RUN: $ PYTHON CFLIST.PY

import subprocess
import json


AUTH_KEY = "<AUTH-KEY>"
AUTH_EMAIL = "<AUTH-EMAIL>"

ACCOUNT_ID = "<ACCOUNT_ID>"
LIST_ID = "<LIST_ID>"

# Check if the requests library is installed
try:
    import requests
except ImportError:
    # Install the requests library
    subprocess.check_call(['pip', 'install', 'requests'])
    import requests

# Set the initial cursor value to retrieve the first page of items
CURSOR = ""
mycursor = ""
url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/rules/lists/{LIST_ID}/items"
all_items = []

# Use a while loop to iterate over all response pages
while True:
    # Send a request to the Cloudflare API and retrieve the current page of list items
    response = requests.get(
        url,
        params={"cursor": mycursor},
        headers={"Content-Type": "application/json", "X-Auth-Key": f"{AUTH_KEY}", "X-Auth-Email": f"{AUTH_EMAIL}"}
    )
  
    # Check if there are any errors in the response
    if response.status_code != 200:
        print(f"Error retrieving list items. Status code: {response.status_code}")
        print(response.content)
        exit(1)

    # Extract and process the items
    items = response.json()["result"]
    print(f"Page {mycursor} items:")
    print(items)

    # Add items to the list of all items
    all_items += items

    # Check if there are more items to retrieve
    result_info = response.json()["result_info"]
    cursors = result_info.get("cursors")
    if not cursors or "after" not in cursors:
        print("Reached the end of the list.")
        break
    else:
        mycursor = cursors["after"]

# Write all items to a file
with open("items.json", "w") as f:
    json.dump(all_items, f)

print(f"Retrieved {len(all_items)} items and saved to items.json")
