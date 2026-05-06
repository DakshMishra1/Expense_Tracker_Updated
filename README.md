# Expense Tracker – Setup Guide

## What was fixed

| File | Problem | Fix |
|------|---------|-----|
| `users.json` | Passwords stored in **plain text** – login always failed on the web | All passwords re-hashed with `werkzeug` |
| `user_data.json` | `testuser` had a `null` entry that caused API crashes | Replaced with valid empty structure |
| `utils.py` | File paths were relative to the **working directory**, so data files were not found when Flask was started from another folder | Paths now anchored to the script's own directory |
| `login.py` | Used its own `USER_FILE = "users.json"` constant instead of the one from `utils.py` | Now imports `USER_FILE` from `utils.py` |
| `api.py` | `get_json()` without `silent=True` could raise on bad input; null user-data not guarded | Added `silent=True` everywhere; `get_session_data()` now auto-heals a null entry |
| `serve.py` | Hard-coded filename with spaces/parentheses broke URL routing | Auto-detects the HTML file; prefers `expense_tracker.html` |

---

## Quick start

### 1 – Install dependencies (once)
```
pip install flask flask-cors werkzeug
```

### 2 – Copy fixed files into your project folder
Replace the originals with the files provided:
- `users.json`
- `user_data.json`
- `utils.py`
- `login.py`
- `api.py`
- `serve.py`

**Optional but recommended:** rename the HTML file:
```
expense_tracker_gui (1).html  →  expense_tracker.html
```
`serve.py` auto-detects either name, but a clean filename avoids browser issues.

### 3 – Start the API server
```
python api.py
```
You should see:
```
✅  Expense Tracker API  →  http://localhost:5000
```

### 4 – Start the web server (new terminal)
```
python serve.py
```
You should see:
```
✅  Web UI  →  http://localhost:8000
```

### 5 – Open in browser
```
http://localhost:8000
```

---

## Existing account passwords (after fix)

| Username | Password |
|----------|----------|
| Daksh Mishra | `123456789` |
| Daksh | `1234` |
| piyush | `123456789` |
| daksh | `123456789` |
| testuser | `password123` |
| testwebuser | `testwebuser123` |

---

## Creating a new account
Use the **Register** tab in the web UI – passwords are hashed automatically.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Cannot reach API" in browser | Flask not running | Run `python api.py` first |
| Login always says "Invalid username or password" | Old `users.json` with plain-text passwords | Replace with the fixed `users.json` |
| Data not saved between restarts | Flask started from wrong directory | Always run from the project folder, or use the fixed `utils.py` which uses absolute paths |
| CORS error in browser console | Opening HTML as `file://` instead of `http://` | Use `serve.py` – always open via `http://localhost:8000` |
