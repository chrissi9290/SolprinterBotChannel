import requests
import json

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

def api_daten_check(tokens):
    print("=== API Daten Check ===")
    for i, token in enumerate(tokens[:3]):  # Nur 3 Tokens zeigen
        print(f"\n--- Token {i+1} ---")
        print(json.dumps(token, indent=4))

def main():
    tokens = hole_neue_tokens()
    api_daten_check(tokens)

if __name__ == "__main__":
    main()