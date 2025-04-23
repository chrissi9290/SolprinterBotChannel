# Nur Test, Preise für bekannte Tokens
test_symbols = ['SOL', 'BTC', 'USDC']
prices = get_cmc_prices(test_symbols)

for symbol in test_symbols:
    print(f"{symbol}: ${prices.get(symbol, 'n/a')}")