import requests
import time
import threading

# Neuer Bot-Token & Gruppen-ID
BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'  # Deine Gruppe SOLPRINTER PONZI

bekannte_paare = set()

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    response = requests.post(url, data=payload)
    print(f"Telegram Response: {response.status_code}, {response.text}")

# Testnachricht beim Start
sende_telegram_nachricht("Bot wurde erfolgreich gestartet und läuft!")

def checke_neue_coins():
    global bekannte_paare
    while True:
        try:
            print("Prüfe neue Coins...")
            response = requests.get("https://api.dexscreener.io/latest/dex/pairs")
            data = response.json()
            neue_coins = []

            for pair in data['pairs']:
                pair_id = pair['pairAddress']
                if pair_id not in bekannte_paare:
                    bekannte_paare.add(pair_id)
                    neue_coins.append(pair)

            print(f"{len(neue_coins)} neue Coins gefunden")

            for coin in neue_coins:
                symbol = coin['baseToken']['symbol']
                quote = coin['quoteToken']['symbol']
                price = round(float(coin['priceUsd']), 4)
                pair_url = coin['url']
                nachricht = f"Neuer Coin entdeckt:\n{symbol}/{quote} - ${price}\n{pair_url}"
                sende_telegram_nachricht(nachricht)

        except Exception as e:
            print(f"Fehler beim Check neuer Coins: {e}")

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
thread_neue_coins = threading.Thread(target=checke_neue_coins)
thread_top_10 = threading.Thread(target=poste_top_10)

thread_neue_coins.start()
thread_top_10.start()
