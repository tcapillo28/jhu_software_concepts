from urllib.request import Request, urlopen
import json

url = "https://www.thegradcafe.com/api/admissions.php?q=computer"

req = Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

response = urlopen(req)
data = json.loads(response.read().decode("utf-8"))

print(data)




