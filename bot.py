import requests
import time
import threading

# Bot-Token & Gruppen-ID
BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'  # Deine Gruppe SOLPRINTER PONZI

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    response = requests.post(url, data=payload)
    print(f"Telegram Response: {response.status_code}, {response.text}")

# Testnachricht beim Start
sende_telegram_nachricht("Bot wurde erfolgreich gestartet und läuft!")

def checke_coins_debug():
    while True:
        try:
            print("Prüfe Coins (Debug)...")
            response = requests.get("https://api.dexscreener.io/latest/dex/pairs")
            data = response.json()

            # Debug: Poste einfach die ersten 5 Coins!
            for coin in data['pairs'][:5]:
                symbol = coin['baseToken']['symbol']
                quote = coin['quoteToken']['symbol']
                price = round(float(coin['priceUsd']), 4)
                pair_url = coin['url']
                nachricht = f"Test Coin:\n{symbol}/{quote} - ${price}\n{pair_url}"
                sende_telegram_nachricht(nachricht)

        except Exception as e:
            print(f"Fehler beim Debug-Check der Coins: {e}")

        time.sleep(600)  # 10 Minuten

def poste_top_10():
    while True:
        try:
            print("Poste Top 10 Coins...")
            response = requests.get("https://api.dexscreener.io/latest/dex/pairs")
            data = response.json()

            paare = sorted(data['pairs'], key=lambda x: float(x['volume']['h24Usd']), reverse=True)
            top_10 = paare[:10]

            nachricht = "Top 10 Coins (24h Volumen):\n"
            for i, coin in enumerate(top_10, 1):
                symbol = coin['baseToken']['symbol']
                quote = coin['quoteToken']['symbol']
                price = round(float(coin['priceUsd']), 4)
                volume = round(float(coin['volume']['h24Usd']), 2)
                nachricht += f"{i}. {symbol}/{quote} - ${price} - Vol: ${volume}\n"

            sende_telegram_nachricht(nachricht)

        except Exception as e:
            print(f"Fehler beim Posten der Top 10: {e}")

        time.sleep(3600)  # 60 Minuten

# Starte Threads
thread_debug_coins = threading.Thread(target=checke_coins_debug)
thread_top_10 = threading.Thread(target=poste_top_10)

thread_debug_coins.start()
thread_top_10.start()
