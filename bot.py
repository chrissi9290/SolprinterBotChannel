import requests
import time
from datetime import datetime, timezone, timedelta


BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": nachricht,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def get_new_tokens():
    url = "https://lite-api.jup.ag/tokens/v1/new"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Fehler API: {response.status_code}")
        return []

def get_prices_from_jupiter(mint_addresses):
    url = "https://price.jup.ag/v4/price"
    params = {"ids": ",".join(mint_addresses)}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            prices = {}
            for mint, info in data.get("data", {}).items():
                prices[mint] = info.get("price", None)
            return prices
        else:
            print(f"Fehler Preisabfrage: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Fehler: {e}")
        return {}

def filter_tokens(tokens):
    jetzt = datetime.now(timezone.utc)
    gefiltert = []
    for token in tokens:
        created = datetime.fromtimestamp(token['created_at'], timezone.utc)
        alter = (jetzt - created).total_seconds() / 60  # in Minuten
        if alter <= 120:  # Maximal 2h alt
            gefiltert.append(token)
    return gefiltert[:10]  # Maximal 10 Tokens für Preisabfrage

def main():
    while True:
        print("Hole neue Tokens...")
        tokens = get_new_tokens()
        tokens = filter_tokens(tokens)

        if not tokens:
            print("Keine passenden Tokens gefunden.")
            time.sleep(3600)
            continue

        mints = [t['mint'] for t in tokens]
        preise = get_prices_from_jupiter(mints)

        gesendet = 0
        for token in tokens:
            mint = token['mint']
            preis = preise.get(mint, None)
            if preis is None or preis == 0:
                continue  # Nur Tokens mit Preis

            name = token['name']
            symbol = token['symbol']
            decimals = token['decimals']
            age_min = int((datetime.now(timezone.utc) - datetime.fromtimestamp(token['created_at'], timezone.utc)).total_seconds() / 60)

            chart_link = f"https://dexscreener.com/solana/{mint}"
            swap_link = f"https://jup.ag/swap/SOL-{mint}"

            nachricht = f"""🆕 *Neues Token auf Jupiter:*
*{name}* ({symbol})
*Address:* `{mint}`
*Decimals:* {decimals}
*Preis:* ${preis:.6f}
*Alter:* {age_min} Min.
[📈 Chart]({chart_link}) | [🔄 Swap]({swap_link})"""

            sende_telegram_nachricht(nachricht)
            gesendet += 1
            if gesendet >= 5:
                break

        time.sleep(3600)  # Alle 60 Minuten ausführen

if __name__ == "__main__":
    main()