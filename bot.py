import requests
import time
import json

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

CMC_API_KEY = '99028e78-8d31-4988-82f6-7d625fcb7304'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    try:
        requests.post(url, data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Telegram Fehler: {e}")

def get_cmc_prices(symbols):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': ','.join(symbols),
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }
    session = requests.Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', {})
            return {symbol: round(data[symbol]['quote']['USD']['price'], 6) for symbol in data}
    except Exception as e:
        print(f"CMC Fehler: {e}")
    return {}

sende_telegram_nachricht("🔥 Jupiter Bot mit CoinMarketCap Preise gestartet!")

while True:
    try:
        response = requests.get("https://lite-api.jup.ag/tokens/v1/new", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tokens = data[:5]

            symbols = [token.get('symbol', '').upper() for token in tokens if token.get('symbol')]
            prices = get_cmc_prices(symbols)

            for token in tokens:
                name = token.get('name', '???')
                symbol = token.get('symbol', '???').upper()
                address = token.get('mint', '???')
                decimals = token.get('decimals', '???')
                preis = prices.get(symbol, 'n/a')

                nachricht = (
                    f"🆕 Neues Token auf Jupiter:\n"
                    f"{name} ({symbol})\n"
                    f"Address: {address}\n"
                    f"Decimals: {decimals}\n"
                    f"Preis: ${preis}"
                )
                sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Jupiter Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(900)  # alle 15 Minuten neue Tokens checken