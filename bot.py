import requests
import time

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'
BIRDEYE_API_KEY = '1c68ac943a2a423d91e73f1617b8ddf5'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    requests.post(url, data=payload)

sende_telegram_nachricht("Birdeye Token Bot gestartet!")

while True:
    try:
        headers = {'X-API-KEY': BIRDEYE_API_KEY}
        response = requests.get("https://public-api.birdeye.so/public/tokenlist", headers=headers)
        if response.status_code == 200:
            data = response.json()
            tokens = data.get('data', [])[:5]  # Nur die ersten 5 Tokens

            nachricht = "🔥 Birdeye Tokens:\n"
            for token in tokens:
                name = token.get('name', 'Unbekannt')
                symbol = token.get('symbol', '')
                price = round(float(token.get('priceUsd', 0)), 4)
                nachricht += f"{name} ({symbol}) - ${price}\n"

            sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Birdeye Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(600)  # alle 10 Minuten