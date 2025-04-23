import requests
import time
from datetime import datetime, timezone

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'
JUPITER_NEW_TOKENS_URL = 'https://lite-api.jup.ag/tokens/v1/new'

def ist_token_neu(created_at_timestamp):
    try:
        created_dt = datetime.fromtimestamp(int(float(created_at_timestamp)), tz=timezone.utc)
        now = datetime.now(timezone.utc)
        diff = (now - created_dt).total_seconds() / 60
        return diff <= 60
    except Exception as e:
        print(f"Timestamp Fehler: {e}")
        return False

def sende_telegram_nachricht(nachricht):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': nachricht, 'parse_mode': 'HTML'}
    try:
        response = requests.post(url, data=payload)
        print(response.text)
    except Exception as e:
        print(f"Telegram Fehler: {e}")

def hole_neue_tokens():
    try:
        print("Hole neue Tokens...")
        response = requests.get(JUPITER_NEW_TOKENS_URL)
        tokens = response.json()
        
        for token in tokens:
            if ist_token_neu(token.get('created_at')) and token.get('price', 0) > 0:
                name = token.get('name', 'N/A')
                symbol = token.get('symbol', 'N/A')
                address = token.get('mint', '???')
                decimals = token.get('decimals', 'N/A')
                price = round(float(token.get('price', 0)), 6)
                market_cap = round(float(token.get('market_cap', 0)), 2)
                liquidity = round(float(token.get('liquidity', 0)), 2)

                swap_link = f"https://jup.ag/swap/SOL-{address}"
                chart_link = f"https://birdeye.so/token/{address}?chain=solana"

                nachricht = (
                    f"🆕 Neues Token auf Jupiter:\n"
                    f"<b>{name} ({symbol})</b>\n"
                    f"Address: <code>{address}</code>\n"
                    f"Decimals: {decimals}\n"
                    f"Preis: ${price}\n"
                    f"MarketCap: ${market_cap}\n"
                    f"Liquidity: ${liquidity}\n\n"
                    f"<a href='{swap_link}'>Swap Now</a> | <a href='{chart_link}'>Chart</a>"
                )
                sende_telegram_nachricht(nachricht)

    except Exception as e:
        print(f"Fehler: {e}")
        sende_telegram_nachricht(f"Fehler: {e}")

if __name__ == '__main__':
    while True:
        hole_neue_tokens()
        time.sleep(900)  # Alle 15 Minuten