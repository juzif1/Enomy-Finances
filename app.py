
import os
from datetime import datetime

import psycopg2
from bottle import (Bottle, error, redirect, request, response, run,
                    static_file, template)

from auth import get_current_user, hash_password, login_user, logout_user
from config import DB_CONFIG
from currency import get_exchange_rates
from investments import calculate

app = Bottle()


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def log_error(message):
    user_id = get_current_user()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO error_logs (user_id, error_message, created_at) "
            "VALUES (%s, %s, %s)",
            (user_id, message, datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        with open("error_fallback.log", "a") as f:
            f.write(f"{datetime.now()} | {user_id} | {message}\n")


def login_required():
    if not get_current_user():
        redirect('/login')



@app.route('/')
def index():
    return template('index')



@app.route('/register', method=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash, created_at) "
                "VALUES (%s, %s, %s)",
                (username, hash_password(password), datetime.now())
            )
            conn.commit()
            return template('result', message="Registration successful.")
        except Exception as e:
            log_error(str(e))
            return template('result', message="Username already exists.")
        finally:
            cur.close()
            conn.close()

    return template('register')


@app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, password_hash FROM users WHERE username = %s",
            (username,)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()

        if not user or user[1] != hash_password(password):
            return template('result', message="Invalid username or password.")

        session_id = login_user(user[0])
        response.set_cookie("session_id", session_id, httponly=True)
        redirect('/')

    return template('login')


@app.route('/logout')
def logout():
    logout_user()
    response.delete_cookie("session_id")
    redirect('/login')



def calculate_fee(amount):
    if amount <= 500:
        return amount * 0.035
    elif amount <= 1500:
        return amount * 0.027
    elif amount <= 2500:
        return amount * 0.02
    else:
        return amount * 0.015


@app.route('/currency', method=['GET', 'POST'])
def currency_conversion():
    login_required()

    if request.method == 'POST':
        try:
            amount = float(request.forms.get('amount'))
            src = request.forms.get('source_currency')
            tgt = request.forms.get('target_currency')

            if amount < 300 or amount > 5000:
                return template(
                    'result',
                    message="Transaction amount must be between £300 and £5000."
                )

            fee = calculate_fee(amount)
            rates = get_exchange_rates()
            converted = (amount - fee) * (rates[tgt] / rates[src])

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO transactions
                   (user_id, source_currency, target_currency,
                    amount, fee, result, created_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    get_current_user(), src, tgt,
                    amount, fee, converted, datetime.now()
                )
            )
            conn.commit()
            cur.close()
            conn.close()

            return template(
                'result',
                message=f"Converted Amount: £{converted:.2f} (Fee: £{fee:.2f})"
            )

        except Exception as e:
            log_error(str(e))
            return template('result', message="Currency conversion failed.")

    return template('currency')



@app.route('/investment', method=['GET', 'POST'])
def investment():
    login_required()

    if request.method == 'POST':
        try:
            investment_type = request.forms.get('investment_type')
            lump_sum = float(request.forms.get('lump_sum', 0))
            monthly = float(request.forms.get('monthly_investment', 0))

            configs = {
                "Basic Savings Plan": {
                    "rate_min": 0.012,
                    "rate_max": 0.024,
                    "fee_rate": 0.0025,
                    "tax": []
                },
                "Savings Plan Plus": {
                    "rate_min": 0.03,
                    "rate_max": 0.055,
                    "fee_rate": 0.003,
                    "tax": [(12000, 0.10)]
                },
                "Managed Stock Investments": {
                    "rate_min": 0.04,
                    "rate_max": 0.23,
                    "fee_rate": 0.013,
                    "tax": [(40000, 0.20), (12000, 0.10)]
                }
            }

            cfg = configs[investment_type]
            results = {}

            for years in (1, 5, 10):
                r = calculate(
                    lump_sum,
                    monthly,
                    years,
                    cfg["rate_min"],
                    cfg["rate_max"],
                    cfg["fee_rate"],
                    cfg["tax"]
                )
                results[years] = r

                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute(
                    """INSERT INTO investment_quotes
                       (user_id, investment_type, years,
                        min_value, max_value,
                        profit_min, profit_max,
                        fees, tax_min, tax_max, created_at)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (
                        get_current_user(), investment_type, years,
                        r["min"], r["max"],
                        r["profit_min"], r["profit_max"],
                        r["fees"], r["tax_min"], r["tax_max"],
                        datetime.now()
                    )
                )
                conn.commit()
                cur.close()
                conn.close()

            return template('investment_result', results=results)

        except Exception as e:
            log_error(str(e))
            return template(
                'result',
                message="Investment calculation failed."
            )

    return template('investment')



@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.path.join(os.getcwd(), 'static'))



@error(500)
def error500(err):
    log_error(str(err))
    return template(
        'result',
        message="Internal server error. Please try again later."
    )


if __name__ == '__main__':
    print(get_exchange_rates())  # Test exchange rate fetching
    run(app, host='localhost', port=8080, debug=True)
