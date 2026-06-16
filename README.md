# Credit Card Expense Tracker

A simple, mobile-friendly Flask app for tracking credit card expenses in Hebrew. Automatically alerts when expenses exceed 850 NIS and supports passwordless expense entry with admin-only reset.

## Features

- 💳 Simple expense tracking with real-time totals
- 📧 Email alerts when expenses exceed 850 NIS threshold
- 🔐 Password-protected reset (admin only)
- 🇮🇱 Full Hebrew support with RTL layout
- 📱 Mobile-friendly responsive design
- ⚡ Lightweight Flask app with JSON state storage
- 🚀 Ready for Railway deployment

## Local Testing

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your Gmail credentials

# Run the app
python3 app.py
```

Open http://localhost:5000 in your browser.

## Environment Variables

Required for production:
- `GMAIL_USER` — Gmail address (e.g., yoavalyagon@gmail.com)
- `GMAIL_PASS` — Gmail app-specific password (not your regular password)
- `TO_EMAIL` — Email to receive alerts
- `RESET_PASSWORD` — Password for reset button (set in Railway dashboard)
- `FLASK_ENV` — Set to `production`

## Deployment to Railway

### 1. Create GitHub Repository

```bash
git remote add origin https://github.com/YOUR_USERNAME/credit-card-tracker.git
git branch -M main
git push -u origin main
```

### 2. Connect to Railway

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select the `credit-card-tracker` repository
4. Railway will automatically detect the Procfile and runtime.txt

### 3. Set Environment Variables in Railway

In the Railway dashboard, go to your project and add these variables:

```
GMAIL_USER=yoavalyagon@gmail.com
GMAIL_PASS=your_app_specific_password
TO_EMAIL=yoavalyagon@gmail.com
RESET_PASSWORD=your_secure_password
FLASK_ENV=production
```

⚠️ **Important**: Use an [app-specific password](https://support.google.com/accounts/answer/185833) for Gmail, not your regular password.

### 4. Share URL with Kamil

Once deployed, Railway will give you a public URL like `https://credit-card-tracker.up.railway.app`. Share this link with Kamil.

## Usage

**For Kamil (expense entry):**
1. Enter the amount spent
2. Click "הוסף הוצאה" (Add Expense)
3. Alert will notify when total > 850 NIS

**For Yoav (reset after reload):**
1. Click "אפס מונה" (Reset Counter)
2. Enter reset password
3. Counter resets to 0

## Technical Details

- **Framework**: Flask 2.3.3
- **Server**: Gunicorn (production)
- **State Storage**: JSON file in `config/expense_state.json`
- **Email**: Gmail SMTP (smtp.gmail.com:465)
- **UI**: Bootstrap 5 + Custom CSS with RTL support
- **Python**: 3.11.9

## File Structure

```
credit-card-tracker/
├── app.py                    # Flask app (routes + email + state)
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version for Railway
├── Procfile                 # Entry point for Railway
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── config/
│   └── expense_state.json   # Current state (auto-created)
├── static/
│   └── style.css            # Styling
└── templates/
    └── index.html           # HTML template (Hebrew UI)
```

## License

Private use only.
