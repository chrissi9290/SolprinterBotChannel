import requests
from datetime import datetime

# Telegram Bot Config
BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def hole_neue_tokens():
    url = "https://lite-api.jup.ag/tokens/v1/new"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Fehler bei API Anfrage: {e}")
        return []

def filter_tokens(tokens):
    gefiltert = []
    jetzt = datetime.utcnow()
    for token in tokens:
        try:
            erstellt = datetime.utcfromtimestamp(int(token['created_at']))
            alter_minuten = int((jetzt - erstellt).total_seconds() / 60)
            preis = float(token.get('price', 0))
            liquidity = float(token.get('liquidity', 0))
            if alter_minuten <= 120 and preis > 0 and liquidity >= 1000:
                token['alter_minuten'] = alter_minuten
                gefiltert.append(token)
        except Exception as e:
            print(f"Fehler beim Filtern: {e}")
    return gefiltert[:5]  # Maximal 5 Tokens

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": nachricht, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Fehler beim Senden: {e}")

def main():
    print("Hole neue Tokens...")
    tokens = hole_neue_tokens()
    neue_tokens = filter_tokens(tokens)
    print(f"Gefundene neue Tokens mit Preis & Liquidity: {len(neue_tokens)}")

    for token in neue_tokens:
        preis = round(float(token.get('price', 0)), 6)
        market_cap = token.get('market_cap')
        liquidity = token.get('liquidity')
        market_cap_display = f"${round(float(market_cap), 2)}" if market_cap else "n/a"
        liquidity_display = f"${round(float(liquidity), 2)}" if liquidity else "n/a"
        alter = token.get('alter_minuten', '?')
        mint = token.get('mint', '?')
        chart_link = f"https://birdeye.so/token/{mint}?chain=solana"
        swap_link = f"https://jup.ag/swap/SOL-{mint}"

        nachricht = (
            f"🆕 Neues Token auf Jupiter:\n"
            f"*{token['name']}* ({token['symbol']})\n"
            f"Address: `{mint}`\n"
            f"Decimals: {token['decimals']}\n"
            f"Preis: ${preis}\n"
            f"MarketCap: {market_cap_display}\n"
            f"Liquidity: {liquidity_display}\n"
            f"Alter: {alter} Min.\n"
            f"[📈 Chart]({chart_link}) | [🔄 Swap]({swap_link})"
        )
        sende_telegram_nachricht(nachricht)

if __name__ == "__main__":
    main()