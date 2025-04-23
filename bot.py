import requests
import time

# === Telegram Settings ===
BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'
CMC_API_KEY = '99028e78-8d31-4988-82f6-7d625fcb7304'

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

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
        print(f"CMC Error: {e}")
    return {}

def is_token_new(created_at_timestamp, limit_minutes=60):
    now = int(time.time())
    age = now - int(created_at_timestamp)
    return age <= limit_minutes * 60

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
                price = prices.get(symbol)

                if not is_token_new(created_at):
                    continue  # Too old → skip
                if price is None or price == 'n/a':
                    continue  # No price → skip

                message = (
                    f"🆕 *New Token Listed on Jupiter:*\n"
                    f"*{name}* ({symbol})\n"
                    f"*Address:* `{address}`\n"
                    f"*Decimals:* {decimals}\n"
                    f"*Price:* ${price}\n\n"
                    f"[➡️ Swap on Jupiter](https://jup.ag/swap/SOL-{address})\n"
                    f"[📈 View Chart](https://birdeye.so/token/{address}?chain=solana)"
                )
                send_telegram_message(message)

        else:
            send_telegram_message(f"Jupiter Error: HTTP {response.status_code}")

    except Exception as e:
        send_telegram_message(f"Error: {e}")

    time.sleep(3600)  # 60 minutes pause