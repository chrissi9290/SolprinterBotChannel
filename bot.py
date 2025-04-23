import requests
import time
from datetime import datetime, timedelta

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": nachricht, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def hole_tokens():
    url = "https://lite-api.jup.ag/tokens/v1/new"
    response = requests.get(url)
    return response.json()

def hole_preise(token_ids):
    url = f"https://price.jup.ag/v4/price?ids={','.join(token_ids)}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("data", {})
    return {}

def main():
    try:
        sende_telegram_nachricht("🔥 Jupiter Token Bot läuft! 🔥")
        tokens_data = hole_tokens()
        now = datetime.utcnow()
        gefilterte_tokens = []

        for token in tokens_data:
            created_at_ts = int(token.get('created_at', 0))
            created_at = datetime.utcfromtimestamp(created_at_ts)
            alter = (now - created_at).total_seconds() / 60  # Alter in Minuten

            if alter <= 120:  # Nur Tokens max. 2 Stunden alt
                gefilterte_tokens.append(token)

        if not gefilterte_tokens:
            sende_telegram_nachricht("Keine neuen Tokens gefunden.")
            return

        token_ids = [t['mint'] for t in gefilterte_tokens]
        preise_data = hole_preise(token_ids)

        nachrichten = []
        for token in gefilterte_tokens[:5]:  # max 5 Tokens
            mint = token['mint']
            name = token['name']
            symbol = token['symbol']
            decimals = int(token.get('decimals', 0))
            preis_info = preise_data.get(mint)

            if not preis_info:
                continue

            preis = preis_info.get('price', 0)
            liquiditaet = preis_info.get('liquidity', 0)
            if preis <= 0 or liquiditaet < 1000:
                continue

            alter_minuten = int((now - datetime.utcfromtimestamp(int(token['created_at']))).total_seconds() / 60)
            chart_link = f"https://dexscreener.com/solana/{mint}"
            swap_link = f"https://jup.ag/swap?outputCurrency={mint}"

            nachricht = (
                f"🆕 <b>Neues Token auf Jupiter:</b>\n"
                f"<b>{name}</b> ({symbol})\n"
                f"Address: <code>{mint}</code>\n"
                f"Decimals: {decimals}\n"
                f"Preis: ${preis:.4f}\n"
                f"Liquidity: ${liquiditaet:.2f}\n"
                f"Alter: {alter_minuten} Min.\n"
                f"📈 <a href='{chart_link}'>Chart</a> | 🔄 <a href='{swap_link}'>Swap</a>"
            )
            nachrichten.append(nachricht)

        if nachrichten:
            for msg in nachrichten:
                sende_telegram_nachricht(msg)
        else:
            sende_telegram_nachricht("Keine Tokens mit Preis & Liquidität gefunden.")
    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

# Alle 60 Minuten ausführen
while True:
    main()
    time.sleep(3600)  # 60 Minuten warten