import requests
import time

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    requests.post(url, data=payload)

sende_telegram_nachricht("🔥 Jupiter New Token Bot gestartet!")

while True:
    try:
        response = requests.get("https://lite-api.jup.ag/tokens/v1/new")
        if response.status_code == 200:
            data = response.json()
            tokens = data[:5]  # Direkt die Liste nehmen

            for token in tokens:
                name = token.get('name', '???')
                symbol = token.get('symbol', '???')
                address = token.get('mintAddress', '???')
                decimals = token.get('decimals', '???')
                price = round(float(token.get('price', 0)), 6)
                marketcap = round(float(token.get('marketCap', 0)), 2)
                liquidity = round(float(token.get('liquidity', 0)), 2)

                nachricht = (
                    f"🆕 Neues Token auf Jupiter:\n"
                    f"{name} ({symbol})\n"
                    f"Address: {address}\n"
                    f"Decimals: {decimals}\n"
                    f"Preis: ${price}\n"
                    f"MarketCap: ${marketcap}\n"
                    f"Liquidity: ${liquidity}"
                )
                sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Jupiter Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(900)  # alle 15 Minuten neue Tokens checken