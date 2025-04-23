import time

# Funktion: Ist Token frisch?
def ist_token_neu(created_at_timestamp, limit_minuten=60):
    jetzt = int(time.time())
    alter = jetzt - int(created_at_timestamp)
    return alter <= limit_minuten * 60

# Haupt-Loop: Nur neue Tokens mit Preis
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
        f"🆕 Frisch gelistet auf Jupiter:\n"
        f"{name} ({symbol})\n"
        f"Address: {address}\n"
        f"Decimals: {decimals}\n"
        f"Preis: ${preis}"
    )
    sende_telegram_nachricht(nachricht)