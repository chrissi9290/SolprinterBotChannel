import requests

url = "https://token.jup.ag/new"

response = requests.get(url)

print(response.status_code)
print(response.json())