import requests
import time
import threading

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    try:
        response = requests.post(url, data=payload)
        print(f"Telegram Response: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Fehler beim Senden: {e}")

sende_telegram_nachricht("Raydium Bot gestartet!")

# Raydium Top Pools posten
def checke_raydium_top_pools():
    while True:
        try:
            response = requests.get("https://api.raydium.io/v2/main/pairs")
            if response.status_code == 200:
                data = response.json()

                pools = list(data.values())[:10]  # Nur 10 Pools für wenig Speicher

                nachricht = "🔥 Top Raydium Pools:\n"
                for pool in pools:
                    name = pool.get('name', 'Unbekannt')
                    price = round(float(pool.get('price', 0)), 4)
                    vol = round(float(pool.get('volume24hQuote', 0)), 2)
                    nachricht += f"{name}\nPrice: ${price} | 24h Vol: ${vol}\n\n"

                sende_telegram_nachricht(nachricht)

            else:
                sende_telegram_nachricht(f"Raydium HTTP Fehler: {response.status_code}")

        except Exception as e:
            sende_telegram_nachricht(f"Raydium Fehler: {e}")

        time.sleep(1800)  # Alle 30 Minuten

# Starte den schlanken Raydium-Thread
thread_raydium_top = threading.Thread(target=checke_raydium_top_pools)
thread_raydium_top.start()