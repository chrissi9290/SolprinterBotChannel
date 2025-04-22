import requests
import time
import threading
import datetime

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    response = requests.post(url, data=payload)
    print(f"Telegram Response: {response.status_code}, {response.text}")

sende_telegram_nachricht("Bot wurde erfolgreich gestartet und läuft!")

def checke_neue_coins():
    while True:
        try:
            print("Prüfe neue Coins (Solana)...")
            response = requests.get("https://api.dexscreener.com/latest/dex/pairs/solana")
            data = response.json()

            jetzt = int(time.time() * 1000)  # Aktuelle Zeit in ms
            vor_30_min = jetzt - (30 * 60 * 1000)  # Coins der letzten 30 Minuten

            neue_coins = [
                pair for pair in data['pairs']
                if pair['pairCreatedAt'] and pair['pairCreatedAt'] > vor_30_min
            ]

            print(f"{len(neue_coins)} neue Coins gefunden")
            for coin in neue_coins:
                symbol = coin['baseToken']['symbol']
                quote = coin['quoteToken']['symbol']
                price = round(float(coin['priceUsd']), 4)
                pair_url = coin['url']
                timestamp = datetime.datetime.fromtimestamp(coin['pairCreatedAt'] / 1000).strftime('%Y-%m-%d %H:%M')
                nachricht = f"Neuer Coin:\n{symbol}/{quote} - ${price}\nListed: {timestamp}\n{pair_url}"
                sende_telegram_nachricht(nachricht)

        except Exception as e:
            print(f"Fehler neue Coins: {e}")
            sende_telegram_nachricht(f"Fehler neue Coins: {e}")

        time.sleep(600)  # Alle 10 Minuten prüfen

def poste_top_coins():
    while True:
        try:
            print("Poste Top 10 Coins nach Volumen...")
            response = requests.get("https://api.dexscreener.com/latest/dex/pairs/solana")
            data = response.json()

            paare = sorted(data['pairs'], key=lambda x: float(x['volume']['h24Usd']), reverse=True)
            top_10 = paare[:10]

            nachricht = "Top 10 Solana Coins (24h Volumen):\n"
            for i, coin in enumerate(top_10, 1):
                symbol = coin['baseToken']['symbol']
                quote = coin['quoteToken']['symbol']
                price = round(float(coin['priceUsd']), 4)
                volume = round(float(coin['volume']['h24Usd']), 2)
                nachricht += f"{i}. {symbol}/{quote} - ${price} - Vol: ${volume}\n"

            sende_telegram_nachricht(nachricht)

        except Exception as e:
            print(f"Fehler Top Coins: {e}")
            sende_telegram_nachricht(f"Fehler Top Coins: {e}")

        time.sleep(3600)  # Alle 60 Minuten

# Starte beide Tasks
thread_neue_coins = threading.Thread(target=checke_neue_coins)
thread_top_coins = threading.Thread(target=poste_top_coins)

thread_neue_coins.start()
thread_top_coins.start()