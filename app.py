import os
import json
import smtplib
import threading
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# State file location - Railway uses /app as working directory
CONFIG_DIR = Path('config')
STATE_FILE = CONFIG_DIR / 'expense_state.json'

GMAIL_USER = os.getenv('GMAIL_USER', 'yoavalyagon@gmail.com')
GMAIL_PASS = os.getenv('GMAIL_PASS')
TO_EMAIL = os.getenv('TO_EMAIL', 'yoavalyagon@gmail.com')
RESET_PASSWORD = os.getenv('RESET_PASSWORD', 'default')
THRESHOLD = 850.0


def load_state():
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except Exception as e:
        print(f"Error loading state: {e}")
    return {"total": 0.0, "last_updated": None, "alert_sent": False}


def save_state(state):
    try:
        CONFIG_DIR.mkdir(exist_ok=True, parents=True)
        STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error saving state: {e}")
        raise


def send_alert_email(total):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Alert: Credit card expenses exceeded 850 NIS (Total: {total})"
        msg["From"] = GMAIL_USER
        msg["To"] = TO_EMAIL

        body = f"""
        <html><body style="font-family:Arial;max-width:600px">
        <h2 style="color:#d32f2f">⚠️ Alert: Credit Card Expenses Exceeded Limit</h2>
        <p style="font-size:16px">
            <strong>Total Amount:</strong> {total} NIS<br>
            <strong>Limit:</strong> 850 NIS<br>
        </p>
        <p style="color:#666;font-size:14px">
            Please review your expenses and reload the card when needed.
        </p>
        </body></html>
        """

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=5) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.sendmail(GMAIL_USER, TO_EMAIL, msg.as_string())
        print(f"Alert email sent for total {total}")
        return True
    except Exception as e:
        print(f"Email error (non-blocking): {e}")
        return False


@app.route('/')
def index():
    state = load_state()
    return render_template('index.html', total=state['total'])


@app.route('/api/state', methods=['GET'])
def get_state():
    state = load_state()
    return jsonify(state)


@app.route('/api/add-expense', methods=['POST'])
def add_expense():
    try:
        data = request.json or {}
        amount = float(data.get('amount', 0))

        if amount <= 0:
            return jsonify({'error': 'Invalid amount'}), 400

        state = load_state()
        state['total'] += amount
        state['last_updated'] = datetime.now().isoformat()

        alert_sent = False
        if state['total'] > THRESHOLD and not state.get('alert_sent'):
            state['alert_sent'] = True
            alert_sent = True
            # Send email in background thread (non-blocking)
            thread = threading.Thread(target=send_alert_email, args=(state['total'],))
            thread.daemon = True
            thread.start()

        save_state(state)
        return jsonify({
            'success': True,
            'total': state['total'],
            'alert_sent': alert_sent
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_counter():
    try:
        state = {
            'total': 0.0,
            'last_updated': datetime.now().isoformat(),
            'alert_sent': False
        }
        save_state(state)
        return jsonify({'success': True, 'total': 0.0})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False, port=int(os.getenv('PORT', 5000)))
