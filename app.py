
import os
from datetime import datetime

import psycopg2
from bottle import Bottle, error, run, static_file, template

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
