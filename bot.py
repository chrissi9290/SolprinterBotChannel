import requests
import time

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'
BIRDEYE_API_KEY = '1c68ac943a2a423d91e73f1617b8ddf5'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    requests.post(url, data=payload)

sende_telegram_nachricht("Birdeye Solana Bot gestartet!")

while True:
    try:
        headers = {'X-API-KEY': BIRDEYE_API_KEY}
        response = requests.get("https://public-api.birdeye.so/public/latest-pairs", headers=headers)
        if response.status_code == 200:
            data = response.json()
            pairs = data.get('data', [])[:5]  # Nur die neuesten 5 Paare

            for pair in pairs:
                base = pair.get('baseTokenSymbol')
                quote = pair.get('quoteTokenSymbol')
                price = round(float(pair.get('priceUsd', 0)), 4)
                dex = pair.get('dexName')
                link = pair.get('txUrl', '')
                nachricht = f"🆕 Neuer Solana Coin:\n{base}/{quote} - ${price} auf {dex}\n{link}"
                sende_telegram_nachricht(nachricht)

        else:
            sende_telegram_nachricht(f"Birdeye Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(600)  # alle 10 Minuten