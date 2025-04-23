import requests

url = "https://public-api.birdeye.so/defi/v2/tokens/new_listing?limit=1"
headers = {
    "accept": "application/json",
    "x-chain": "solana",
    "X-API-KEY": "bb5b2f48c9154f69a85c46fa08c83b38"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.text)