import requests
import time

BOT_TOKEN = '7903108939:AAFqZR12Sa8MuL14zgmmRMwsU7FEgQXycjE'
CHAT_ID = '-1002397010517'

def sende_telegram_nachricht(nachricht):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': nachricht}
    requests.post(url, data=payload)

sende_telegram_nachricht("Jupiter Solana Bot gestartet!")

while True:
    try:
        response = requests.get("https://price.jup.ag/v4/price?ids=SOL,USDC")
        if response.status_code == 200:
            data = response.json()
            sol_price = round(float(data['data']['SOL']['price']), 4)
            usdc_price = round(float(data['data']['USDC']['price']), 4)

            nachricht = f"🔥 Solana Preis: ${sol_price}\nUSDC Preis: ${usdc_price}"
            sende_telegram_nachricht(nachricht)
        else:
            sende_telegram_nachricht(f"Jupiter Fehler: HTTP {response.status_code}")

    except Exception as e:
        sende_telegram_nachricht(f"Fehler: {e}")

    time.sleep(600)