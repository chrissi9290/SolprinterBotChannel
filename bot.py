import requests

url = "https://lite-api.jup.ag/tokens/v1/new"
headers = {
    "accept": "application/json"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)