import requests
import time

# === Telegram Einstellungen ===
BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

# === CoinMarketCap API ===
CMC_API_KEY = '99028e78-8d31-4988-82f6-7d625fcb7304'

# === Telegram Funktion (mit Markdown Links) ===
def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': nachricht,
        'parse_mode': 'Markdown'
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Telegram Fehler: {e}")

# === CMC Preise holen ===
def get_cmc_prices(symbols):
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

# === Ist Token neu? ===
def ist_token_neu(created_at_timestamp, limit_minuten=60):
    jetzt = int(time.time())
    alter = jetzt - int(created_at_timestamp)
    return alter <= limit_minuten * 60

# === Hauptloop ===
while True:
    try:
        response = requests.get("https://lite-api.jup.ag/tokens/v1/new", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tokens = data[:10]  # max 10 Tokens

            symbols = [token.get('symbol', '').upper() for token in tokens if token.get('symbol')]
            prices = get_cmc_prices(symbols)

            for token in tokens:
                created_at = token.get('created_at', 0)
                if not ist_token_neu(created_at):
                    continue  # Zu alt → skippen

                name = token.get('name', '???')
                symbol = token.get('symbol', '???').upper()
                address = token.get('mint', '???')
                decimals = token.get('decimals', '???')
                preis = prices.get(symbol)

                if preis is None or preis == 'n/a':
                    continue  # Kein Preis → skippen

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
        else:
            sende_telegram_nachricht(f"Jupiter Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(60)  # 15 Minuten Pause