from urllib.request import Request, urlopen
import json

#Access to Gradcafe's API
url = "https://www.thegradcafe.com/api/admissions.php?q=computer"


req = Request(url, headers={ "User-Agent": "Mozilla/5.0" })

# Sending the request and decode the JSON response
response = urlopen(req)
data = json.loads(response.read().decode("utf-8"))

print(json.dumps(data, indent=2))



