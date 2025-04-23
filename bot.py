import requests
from datetime import datetime, timedelta
import time
import json

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
            differenz = jetzt - erstellt
            if differenz <= timedelta(hours=24):  # Nur 24h Filter
                gefiltert.append(token)
        except Exception as e:
            print(f"Fehler beim Filtern: {e}")
    return gefiltert

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
    print(f"API Antwort: {tokens}")

    neue_tokens = filter_tokens(tokens)
    print(f"Gefundene neue Tokens: {len(neue_tokens)}")

    for token in neue_tokens:
        nachricht = f"🆕 Neues Token auf Jupiter:\n*{token['name']}* ({token['symbol']})\nAddress: `{token['mint']}`\nDecimals: {token['decimals']}"
        sende_telegram_nachricht(nachricht)

if __name__ == "__main__":
    main()