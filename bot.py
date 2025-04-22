import requests
import time

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    try:
        requests.post(url, data=payload)
    except:
        pass

sende_telegram_nachricht("Raydium Bot Minimal gestartet!")

# Raydium Top 5 Pools
while True:
    try:
        response = requests.get("https://api.raydium.io/v2/main/pairs")
        if response.status_code == 200:
            data = response.json()
            pools = list(data.values())[:5]  # Nur 5 Pools!

            nachricht = "🔥 Raydium Top Pools:\n"
            for pool in pools:
                name = pool.get('name', 'Unbekannt')
                price = round(float(pool.get('price', 0)), 4)
                vol = round(float(pool.get('volume24hQuote', 0)), 2)
                nachricht += f"{name}\nPrice: ${price} | 24h Vol: ${vol}\n\n"

            sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Raydium Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(1800)  # Nur alle 30 Minuten prüfen