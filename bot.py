import requests
import time
import threading

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    response = requests.post(url, data=payload)
    print(f"Telegram Response: {response.status_code}, {response.text}")

sende_telegram_nachricht("Raydium Bot gestartet!")

# Raydium Paare abrufen
def get_raydium_pairs():
    url = "https://api.raydium.io/v2/main/pairs"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            sende_telegram_nachricht(f"Raydium HTTP Fehler: {response.status_code}")
            return None
    except Exception as e:
        sende_telegram_nachricht(f"Raydium API Fehler: {e}")
        return None

# Neue Pools prüfen (einfachste Variante: nimm die ersten 5 Paare)
def checke_neue_raydium_pools():
    while True:
        data = get_raydium_pairs()
        if data:
            pools = list(data.values())  # Daten sind als dict mit Paar-Adressen als Keys

            # Sortieren nach TVL oder Volume? Hier: einfach die ersten 5 zeigen
            for pool in pools[:5]:
                base = pool.get('name', 'Unbekannt')
                price = pool.get('price', '0')
                volume = pool.get('volume24hQuote', '0')
                nachricht = f"🆕 Raydium Pool:\n{base}\nPrice: ${price}\n24h Vol: ${volume}"
                sende_telegram_nachricht(nachricht)

        time.sleep(600)  # Alle 10 Minuten

# Starte Thread
thread_raydium = threading.Thread(target=checke_neue_raydium_pools)
thread_raydium.start()