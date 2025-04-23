import requests
import time

# === Telegram Einstellungen ===
BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'
CMC_API_KEY = '99028e78-8d31-4988-82f6-7d625fcb7304'

gepostete_tokens = set()
erste_runde = True  # Alle Tokens einmal posten

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Fehler: {e}")

def get_cmc_prices(symbols):
    if not symbols:
        return {}
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {'symbol': ','.join(symbols), 'convert': 'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': CMC_API_KEY}
    try:
        response = requests.get(url, headers=headers, params=parameters, timeout=10)
        data = response.json().get('data', {})
        return {symbol: round(data[symbol]['quote']['USD']['price'], 6) for symbol in data}
    except Exception as e:
        print(f"CMC Fehler: {e}")
    return {}

def ist_token_neu(created_at_timestamp, limit_minuten=60):
    jetzt = int(time.time())
    alter = jetzt - int(created_at_timestamp)
    return alter <= limit_minuten * 60

while True:
    try:
        response = requests.get("https://lite-api.jup.ag/tokens/v1/new", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tokens = data[:10]

            symbols = [token.get('symbol', '').upper() for token in tokens if token.get('symbol')]
            prices = get_cmc_prices(symbols)

            for token in tokens:
                address = token.get('mint', '???')
                created_at = token.get('created_at', 0)
                name = token.get('name', '???')
                symbol = token.get('symbol', '???').upper()
                decimals = token.get('decimals', '???')
                preis = prices.get(symbol)

                if not ist_token_neu(created_at):
                    continue  # Zu alt → skippen

                if preis is None or preis == 'n/a':
                    continue  # Kein Preis → skippen

                if not erste_runde and address in gepostete_tokens:
                    continue  # Bereits gepostet → skippen

                nachricht = (
                    f"🆕 *Frisch gelistet auf Jupiter:*\n"
                    f"*{name}* ({symbol})\n"
                    f"*Address:* `{address}`\n"
                    f"*Decimals:* {decimals}\n"
                    f"*Preis:* ${preis}\n\n"
                    f"[➡️ Swap bei Jupiter](https://jup.ag/swap/SOL-{address})\n"
                    f"[📈 Chart ansehen](https://birdeye.so/token/{address}?chain=solana)"
                )
                sende_telegram_nachricht(nachricht)
                gepostete_tokens.add(address)

            if erste_runde:
                print("Einmaliger Full-Post abgeschlossen!")
                erste_runde = False  # Ab jetzt nur noch neue Tokens

        else:
            sende_telegram_nachricht(f"Jupiter Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(900)  # 15 Minuten Pause