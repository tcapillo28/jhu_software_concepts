from urllib.request import urlopen
import json

url = "https://www.thegradcafe.com/api/admissions.php?q=computer"

response = urlopen(url)
data = json.loads(response.read().decode("utf-8"))

print(data)





