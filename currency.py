
import requests

STATIC_RATES = {
    'GBP': 1.0,
    'USD': 1.27,
    'EUR': 1.16,
    'BRL': 6.25,
    'JPY': 185.2,
    'TRY': 41.3
}

def get_exchange_rates():
    try:
        res = requests.get(
            "https://api.exchangerate-api.com/v4/latest/GBP",
            timeout=5
        )
        data = res.json()
        return {
            'GBP': 1.0,
            'USD': float(data['rates']['USD']),
            'EUR': float(data['rates']['EUR']),
            'BRL': float(data['rates']['BRL']),
            'JPY': float(data['rates']['JPY']),
            'TRY': float(data['rates']['TRY'])
        }
    except Exception as e:
        print("Exchange rate fetch failed", str(e))
        return STATIC_RATES
