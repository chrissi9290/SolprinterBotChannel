import requests
import time
from datetime import datetime, timezone

# Telegram Config
BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

# CoinMarketCap API Config
CMC_API_KEY = '99028e78-8d31-4988-82f6-7d625fcb7304'

def sende_telegram_nachricht(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def get_cmc_prices(symbols):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }
    parameters = {
        'symbol': ','.join(symbols),
        'convert': 'USD'
    }
    try:
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()
        prices = {}
        for symbol in symbols:
            price_info = data.get('data', {}).get(symbol)
            if price_info:
                prices[symbol] = round(price_info['quote']['USD']['price'], 4)
            else:
                prices[symbol] = 'n/a'
        return prices
    except Exception as e:
        print(f"CMC Fehler: {e}")
        return {}

def ist_token_neu(created_at_timestamp):
    created_dt = datetime.fromtimestamp(created_at_timestamp, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = (now - created_dt).total_seconds() / 60
    return diff <= 60

# Hauptloop
while True:
    try:
        print("Hole neue Tokens...")
        response = requests.get("https://lite-api.jup.ag/tokens/v1/new", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tokens = data[:10]
            print(f"{len(tokens)} Tokens geladen")

            symbols = [token.get('symbol', '').upper() for token in tokens if token.get('symbol')]
            prices = get_cmc_prices(symbols)

            for token in tokens:
                created_at = token.get('created_at', 0)
                if not ist_token_neu(created_at):
                    continue

                name = token.get('name', '???')
                symbol = token.get('symbol', '???').upper()
                address = token.get('mint', '???')
                decimals = token.get('decimals', '???')
                preis = prices.get(symbol)

                if preis == 'n/a' or preis is None:
                    continue

                nachricht = (
                    f"🆕 *Neues Token auf Jupiter:*\n"
                    f"*{name}* ({symbol})\n"
                    f"*Address:* `{address}`\n"
                    f"*Decimals:* {decimals}\n"
                    f"*Preis:* ${preis}\n\n"
                    f"[➡️ Jetzt Swappen](https://jup.ag/swap/SOL-{address})\n"
                    f"[📈 Chart ansehen](https://birdeye.so/token/{address}?chain=solana)"
                )
                sende_telegram_nachricht(nachricht)
        else:
            print(f"Jupiter Fehler HTTP {response.status_code}")
            sende_telegram_nachricht(f"Jupiter Fehler: HTTP {response.status_code}")

    except Exception as e:
        print(f"Fehler: {e}")
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(900)  # alle 15 Minuten