import requests
import time

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'
BIRDEYE_API_KEY = '1c68ac943a2a423d91e73f1617b8ddf5'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    requests.post(url, data=payload)

sende_telegram_nachricht("Birdeye Top Tokens Bot gestartet!")

while True:
    try:
        url = "https://public-api.birdeye.so/defi/tokenlist?sort_by=v24hUSD&sort_type=desc&offset=0&limit=10&min_liquidity=100"
        headers = {
            "accept": "application/json",
            "x-chain": "solana",
            "X-API-KEY": BIRDEYE_API_KEY
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tokens = data.get('data', [])[:10]

            nachricht = "🔥 Top 10 Solana Tokens (24h Volumen):\n"
            for i, token in enumerate(tokens, 1):
                symbol = token.get('symbol', '???')
                price = round(float(token.get('priceUsd', 0)), 6)
                vol = round(float(token.get('v24hUSD', 0)), 2)
                liquidity = round(float(token.get('liquidity', 0)), 2)
                nachricht += f"{i}. {symbol} - ${price} | Vol: ${vol} | LQ: ${liquidity}\n"

            sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Birdeye Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(3600)  # alle 60 Minuten posten