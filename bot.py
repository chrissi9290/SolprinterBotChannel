import requests
import time

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'
BIRDEYE_API_KEY = '1c68ac943a2a423d91e73f1617b8ddf5'

# Token Namen für die Adressen
token_map = {
    "So11111111111111111111111111111111111111112": "SOL",
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": "BONK"  # Beispiel-Token
}

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    requests.post(url, data=payload)

sende_telegram_nachricht("Birdeye Multi-Token Preis Bot gestartet!")

while True:
    try:
        url = "https://public-api.birdeye.so/defi/multi_price"
        payload = { 
            "list_address": ",".join(token_map.keys())
        }
        headers = {
            "accept": "application/json",
            "x-chain": "solana",
            "content-type": "application/json",
            "X-API-KEY": BIRDEYE_API_KEY
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            preise = data.get('data', {})

            nachricht = "🔥 Multi-Token Preise:\n"
            for addr, info in preise.items():
                name = token_map.get(addr, addr[:6])
                price = round(float(info.get('value', 0)), 6)
                nachricht += f"{name}: ${price}\n"

            sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Birdeye Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(600)  # alle 10 Minuten