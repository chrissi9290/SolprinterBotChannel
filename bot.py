import requests
from datetime import datetime, timedelta

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=payload)

def hole_neue_tokens():
    try:
        response = requests.get("https://lite-api.jup.ag/tokens/v1/new", headers={"accept": "application/json"})
        if response.status_code == 200:
            tokens = response.json()
            print(f"API Antwort: {tokens}")  # Debug-Ausgabe
            return tokens
        else:
            print(f"Fehler beim Abrufen: {response.status_code}")
            sende_telegram_nachricht(f"Fehler beim Abrufen der Tokens: {response.status_code}")
            return []
    except Exception as e:
        print(f"Fehler: {e}")
        sende_telegram_nachricht(f"Fehler beim API-Aufruf: {e}")
        return []

def filter_tokens(tokens):
    gefiltert = []
    jetzt = datetime.utcnow()
    for token in tokens:
        try:
            erstellt = datetime.utcfromtimestamp(int(token['created_at']))
            differenz = jetzt - erstellt
            if differenz <= timedelta(hours=24) and float(token.get('price', 0)) > 0:
                gefiltert.append(token)
        except Exception as e:
            print(f"Fehler beim Filtern: {e}")
    return gefiltert

def verarbeite_tokens(tokens):
    for token in tokens:
        try:
            name = token.get('name', '???')
            symbol = token.get('symbol', '???')
            address = token.get('mint', '???')
            decimals = token.get('decimals', '???')
            price = round(float(token.get('price', 0)), 6)
            msg = f"🆕 Neues Token auf Jupiter:\n{name} ({symbol})\nAddress: {address}\nDecimals: {decimals}\nPreis: ${price}"
            sende_telegram_nachricht(msg)
        except Exception as e:
            print(f"Fehler beim Senden: {e}")

# Hauptablauf
print("Bot gestartet, hole neue Tokens...")
alle_tokens = hole_neue_tokens()
gefilterte_tokens = filter_tokens(alle_tokens)
print(f"Gefundene neue Tokens: {len(gefilterte_tokens)}")  # Debug-Ausgabe
verarbeite_tokens(gefilterte_tokens)