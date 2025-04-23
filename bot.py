import requests

response = requests.get("https://lite-api.jup.ag/tokens/v1/new")
if response.status_code == 200:
    data = response.json()
    for token in data[:3]:  # Nur 3 Tokens für Übersicht
        print(token)
else:
    print(f"Fehler: HTTP {response.status_code}")