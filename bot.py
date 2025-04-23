import requests
import time

def get_prices_with_retry(mint_addresses, retries=3, delay=5):
    price_url = f"https://price.jup.ag/v4/price?ids={','.join(mint_addresses)}"
    for attempt in range(retries):
        try:
            price_response = requests.get(price_url, timeout=10)
            if price_response.status_code == 200:
                prices_data = price_response.json().get('data', {})
                return {mint: round(info.get('price', 0), 6) for mint, info in prices_data.items()}
        except requests.exceptions.RequestException as e:
            print(f"Preis-Request Fehler: {e}")
            time.sleep(delay)
    return {}

# Beispiel-Nutzung:
# prices = get_prices_with_retry(mint_addresses)