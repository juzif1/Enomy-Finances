
import os
from datetime import datetime

import psycopg2
from bottle import Bottle, error, request, run, static_file, template

from config import DB_CONFIG

app = Bottle()

# Exchange rates
EXCHANGE_RATES = {
    'GBP': 1.0,
    'USD': 1.27,
    'EUR': 1.16,
    'BRL': 6.25,
    'JPY': 185.2,
    'TRY': 41.3
}

# Logging
def log_error(message):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("INSERT INTO error_logs (error_message, created_at) VALUES (%s, %s)", (message, datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Logging failed: {e}")

# Database connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

# Routes
@app.route('/')
def index():
    return template('index') 

@app.route('/currency', method=['GET', 'POST'])
def currency_conversion():
    if request.method == 'POST':
        try:
            amount = float(request.forms.get('amount'))
            src = request.forms.get('source_currency')
            tgt = request.forms.get('target_currency')

            if amount < 300 or amount > 5000:
                return template('result', message="Amount must be between £300 and £5000.")

            fee = calculate_fee(amount)
            converted_amount = (amount - fee) * (EXCHANGE_RATES[tgt] / EXCHANGE_RATES[src])

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO transactions (source_currency, target_currency, amount, fee, result, created_at) VALUES (%s,%s,%s,%s,%s,%s)",
                (src, tgt, amount, fee, converted_amount, datetime.now())
            )
            conn.commit()
            cur.close()
            conn.close()

            return template('result', message=f"Converted Amount: £{converted_amount:.2f} (Fee: £{fee:.2f})")
        except Exception as e:
            log_error(str(e))
            return template('result', message="An error occurred during conversion.")
    return template('currency')

@app.route('/investment', method=['GET', 'POST'])
def investment_calculator():
    if request.method == 'POST':
        try:
            investment_type = request.forms.get('investment_type')
            lump_sum = float(request.forms.get('lump_sum', 0))
            monthly = float(request.forms.get('monthly_investment', 0))
            years = int(request.forms.get('years', 1))

            if investment_type == 'Basic Savings Plan':
                min_return = lump_sum + (monthly * 12 * years) * 1.012
                max_return = lump_sum + (monthly * 12 * years) * 1.024
            elif investment_type == 'Savings Plan Plus':
                min_return = lump_sum + (monthly * 12 * years) * 1.03
                max_return = lump_sum + (monthly * 12 * years) * 1.055
            elif investment_type == 'Managed Stock Investments':
                min_return = lump_sum + (monthly * 12 * years) * 1.04
                max_return = lump_sum + (monthly * 12 * years) * 1.23
            else:
                return template('result', message="Invalid investment type.")

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO investment_quotes (investment_type, min_return, max_return, created_at) VALUES (%s,%s,%s,%s)",
                (investment_type, min_return, max_return, datetime.now())
            )
            conn.commit()
            cur.close()
            conn.close()

            return template('result', message=f"Projected Return: Min: £{min_return:.2f}, Max: £{max_return:.2f}")
        except Exception as e:
            log_error(str(e))
            return template('result', message="An error occurred during investment calculation.")
    return template('investment')

# Calculate fee
def calculate_fee(amount):
    if amount <= 500:
        return amount * 0.035
    elif amount <= 1500:
        return amount * 0.027
    elif amount <= 2500:
        return amount * 0.02
    else:
        return amount * 0.015

# Static files
@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.path.join(os.getcwd(), 'static'))

# Error handling
@error(500)
def error500(error):
    log_error(str(error))
    return "Internal server error. Please try again."

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
