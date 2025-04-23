import requests
import time


BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    try:
        requests.post(url, data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Telegram Fehler: {e}")

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

sende_telegram_nachricht("🔥 Jupiter New Token Bot gestartet!")

while True:
    try:
        response = requests.get("https://lite-api.jup.ag/tokens/v1/new", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tokens = data[:5]

            mint_addresses = [token.get('mint', '') for token in tokens]

            prices = get_prices_with_retry(mint_addresses)

            for token in tokens:
                name = token.get('name', '???')
                symbol = token.get('symbol', '???')
                address = token.get('mint', '???')
                decimals = token.get('decimals', '???')
                preis = prices.get(address, 'n/a')

                nachricht = (
                    f"🆕 Neues Token auf Jupiter:\n"
                    f"{name} ({symbol})\n"
                    f"Address: {address}\n"
                    f"Decimals: {decimals}\n"
                    f"Preis: ${preis}"
                )
                sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Jupiter Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(900)  # alle 15 Minuten neue Tokens checken