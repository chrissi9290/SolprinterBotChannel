import requests

# Funktion zum Preis-Abruf via CoinMarketCap
def get_cmc_prices(symbols):
    CMC_API_KEY = '99028e78-8d31-4988-82f6-7d625fcb7304'
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': ','.join(symbols),
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }
    session = requests.Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', {})
            return {symbol: round(data[symbol]['quote']['USD']['price'], 6) for symbol in data}
    except Exception as e:
        print(f"CMC Fehler: {e}")
    return {}

# Jetzt testen mit bekannten Symbolen
test_symbols = ['SOL', 'BTC', 'USDC']
prices = get_cmc_prices(test_symbols)

for symbol in test_symbols:
    print(f"{symbol}: ${prices.get(symbol, 'n/a')}")