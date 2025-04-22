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

sende_telegram_nachricht("Bot wurde erfolgreich gestartet und läuft!")

def checke_coins_debug():
    while True:
        try:
            print("Prüfe Coins (Debug)...")
            response = requests.get("https://api.dexscreener.io/latest/dex/pairs")
            data = response.json()

            anzahl_paare = len(data['pairs'])
            print(f"Dexscreener liefert {anzahl_paare} Paare")

            sende_telegram_nachricht(f"Dexscreener liefert {anzahl_paare} Paare")

            for coin in data['pairs'][:5]:
                symbol = coin['baseToken']['symbol']
                quote = coin['quoteToken']['symbol']
                price = round(float(coin['priceUsd']), 4)
                pair_url = coin['url']
                nachricht = f"Test Coin:\n{symbol}/{quote} - ${price}\n{pair_url}"
                sende_telegram_nachricht(nachricht)

        except Exception as e:
            print(f"Fehler beim Debug-Check der Coins: {e}")
            sende_telegram_nachricht(f"Fehler beim Debug: {e}")

        time.sleep(600)  # 10 Minuten

# Nur Debug-Thread für jetzt!
thread_debug_coins = threading.Thread(target=checke_coins_debug)

thread_debug_coins.start()
