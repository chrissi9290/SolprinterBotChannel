import requests
import time

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'
BIRDEYE_API_KEY = 'bb5b2f48c9154f69a85c46fa08c83b38'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    requests.post(url, data=payload)

sende_telegram_nachricht("🔥 Birdeye Neue Listings Bot gestartet!")

while True:
    try:
        url = "https://public-api.birdeye.so/defi/v2/tokens/new_listing?limit=5&meme_platform_enabled=true"
        headers = {
            "accept": "application/json",
            "x-chain": "solana",
            "X-API-KEY": BIRDEYE_API_KEY
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tokens = data.get('data', {}).get('items', [])

            for token in tokens:
                symbol = token.get('symbol', '???')
                name = token.get('name', '')
                liquidity = round(float(token.get('liquidity', 0)), 2)
                source = token.get('source', '???').capitalize()
                listed_at = token.get('liquidityAddedAt', 'N/A')
                nachricht = (
                    f"🆕 Neues Listing:\n"
                    f"Name: {name} ({symbol})\n"
                    f"DEX: {source}\n"
                    f"Liquidity: ${liquidity}\n"
                    f"Gelistet am: {listed_at}"
                )
                sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Birdeye Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(900)  # alle 15 Minuten checken