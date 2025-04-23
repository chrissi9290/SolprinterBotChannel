import requests
import time

# === Hauptloop mit Debug ===
while True:
    try:
        print("Hole neue Tokens...")
        response = requests.get("https://lite-api.jup.ag/tokens/v1/new", timeout=10)
        if response.status_code == 200:
            data = response.json()
            tokens = data[:10]
            print(f"{len(tokens)} Tokens geladen")

            symbols = [token.get('symbol', '').upper() for token in tokens if token.get('symbol')]
            print(f"Symbole: {symbols}")

            prices = get_cmc_prices(symbols)
            print(f"Preise: {prices}")

            for token in tokens:
                created_at = token.get('created_at', 0)
                if not ist_token_neu(created_at):
                    print(f"Token zu alt: {token.get('symbol')}")
                    continue

                name = token.get('name', '???')
                symbol = token.get('symbol', '???').upper()
                address = token.get('mint', '???')
                decimals = token.get('decimals', '???')
                preis = prices.get(symbol)

                if preis is None or preis == 'n/a':
                    print(f"Kein Preis für {symbol}")
                    continue

                nachricht = (
                    f"🆕 *Frisch gelistet auf Jupiter:*\n"
                    f"*{name}* ({symbol})\n"
                    f"*Address:* `{address}`\n"
                    f"*Decimals:* {decimals}\n"
                    f"*Preis:* ${preis}\n\n"
                    f"[➡️ Swap bei Jupiter](https://jup.ag/swap/SOL-{address})\n"
                    f"[📈 Chart ansehen](https://birdeye.so/token/{address}?chain=solana)"
                )
                print(f"Sende Nachricht für {symbol}")
                sende_telegram_nachricht(nachricht)
        else:
            print(f"Jupiter Fehler HTTP {response.status_code}")
            sende_telegram_nachricht(f"Jupiter Fehler: HTTP {response.status_code}")

    except Exception as e:
        print(f"Fehler: {e}")
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(900)