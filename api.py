"""
api.py  –  Flask REST API for the Expense Tracker web app.

Setup:
    pip install flask flask-cors werkzeug
    python api.py

Then in a separate terminal:
    python serve.py

Open http://localhost:8000 in your browser.
"""

import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from functools import wraps
import json
from werkzeug.security import generate_password_hash, check_password_hash

from utils import load_user_data, save_user_data, get_current_date
from Function import data as default_data
from login import load_users, save_users

# ── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)

# Change this to a long random string in production!
app.secret_key = os.environ.get("SECRET_KEY", "expense_tracker_secret_key_change_me")

# Session cookies are same-site=Lax so they travel with the browser fetch
# from serve.py (localhost:8000 → localhost:5000).
app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,   # set True when using HTTPS
)

CORS(
    app,
    supports_credentials=True,
    origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
    ],
)


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def require_login(f):
    """Decorator – rejects requests that have no active session."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if "username" not in session:
            return jsonify({"error": "Not logged in"}), 401
        return f(*args, **kwargs)
    return decorated


def get_session_data():
    """Load the logged-in user's data, falling back to a fresh structure."""
    data = load_user_data(session["username"])
    # Guard: if the stored value is None/null (corrupt entry) return defaults
    if not isinstance(data, dict):
        data = default_data()
        save_user_data(session["username"], data)
    return data


def save_session_data(data):
    save_user_data(session["username"], data)


# ══════════════════════════════════════════════════════════════════════════════
# AUTH  –  /api/register  /api/login  /api/logout  /api/me
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/register", methods=["POST"])
def register():
    body = request.get_json(silent=True) or {}
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400
    if len(password) < 4:
        return jsonify({"error": "Password must be at least 4 characters"}), 400

    users = load_users()
    if username in users:
        return jsonify({"error": "Username already exists"}), 409

    users[username] = {"password": generate_password_hash(password)}
    save_users(users)
    save_user_data(username, default_data())   # give new user a clean slate

    session["username"] = username
    return jsonify({"message": "Account created", "username": username}), 201


@app.route("/api/login", methods=["POST"])
def login():
    body = request.get_json(silent=True) or {}
    username = (body.get("username") or "").strip()
    password = body.get("password") or ""

    users = load_users()
    user = users.get(username)
    if not user or not check_password_hash(user.get("password", ""), password):
        return jsonify({"error": "Invalid username or password"}), 401

    session["username"] = username
    return jsonify({"message": "Login successful", "username": username})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@app.route("/api/me", methods=["GET"])
@require_login
def me():
    """Check whether a session is still alive (used on page refresh)."""
    return jsonify({"username": session["username"]})


# ══════════════════════════════════════════════════════════════════════════════
# DATA  –  /api/data  GET full snapshot
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/data", methods=["GET"])
@require_login
def get_data():
    return jsonify(get_session_data())


# ══════════════════════════════════════════════════════════════════════════════
# EXPENSES  –  POST /api/expenses  |  DELETE /api/expenses/<cat>/<idx>
# ══════════════════════════════════════════════════════════════════════════════

VALID_CATS = ["Food", "Stationary", "Clothes", "Other"]

@app.route("/api/expenses", methods=["POST"])
@require_login
def add_expense():
    body     = request.get_json(silent=True) or {}
    category = body.get("category", "").strip()
    item     = body.get("item", "").strip()
    amount   = body.get("amount")
    date     = body.get("date") or get_current_date()

    if category not in VALID_CATS:
        return jsonify({"error": f"Category must be one of {VALID_CATS}"}), 400
    if not item:
        return jsonify({"error": "Item name required"}), 400
    try:
        amount = float(amount)
        if amount <= 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify({"error": "Amount must be a positive number"}), 400

    user_data = get_session_data()
    user_data[category]["expenses"].append({"item": item, "amount": amount, "date": date})
    save_session_data(user_data)
    return jsonify({"message": "Expense added", "data": user_data}), 201


@app.route("/api/expenses/<category>/<int:idx>", methods=["DELETE"])
@require_login
def delete_expense(category, idx):
    if category not in VALID_CATS:
        return jsonify({"error": "Invalid category"}), 400

    user_data = get_session_data()
    expenses  = user_data[category]["expenses"]

    if idx < 0 or idx >= len(expenses):
        return jsonify({"error": "Expense index out of range"}), 404

    removed = expenses.pop(idx)
    save_session_data(user_data)
    return jsonify({"message": "Expense deleted", "removed": removed, "data": user_data})


# ══════════════════════════════════════════════════════════════════════════════
# LIMITS  –  PUT /api/limits
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/limits", methods=["PUT"])
@require_login
def set_limits():
    body      = request.get_json(silent=True) or {}
    all_cats  = ["Total Amount"] + VALID_CATS
    user_data = get_session_data()
    updated   = []

    for cat in all_cats:
        if cat in body:
            try:
                limit_val = float(body[cat])
                if limit_val < 0:
                    raise ValueError
                user_data[cat]["limit"] = limit_val
                updated.append(cat)
            except (TypeError, ValueError):
                return jsonify({"error": f"Invalid limit value for '{cat}'"}), 400

    save_session_data(user_data)
    return jsonify({"message": f"Limits updated for: {', '.join(updated)}", "data": user_data})


# ══════════════════════════════════════════════════════════════════════════════
# SPENDING  –  GET /api/spending
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/api/spending", methods=["GET"])
@require_login
def spending_summary():
    user_data   = get_session_data()
    total_limit = user_data.get("Total Amount", {}).get("limit", 0)
    total_spent = 0
    categories  = []

    for cat, details in user_data.items():
        if cat == "Total Amount":
            continue
        limit     = details.get("limit", 0)
        spent     = sum(e.get("amount", 0) for e in details.get("expenses", []))
        remaining = limit - spent
        total_spent += spent
        categories.append({
            "category":  cat,
            "limit":     limit,
            "spent":     spent,
            "remaining": remaining,
            "status":    "Within Limit" if remaining >= 0 else "Over Limit",
        })

    return jsonify({
        "total_limit":     total_limit,
        "total_spent":     total_spent,
        "total_remaining": total_limit - total_spent,
        "categories":      categories,
    })


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("✅  Expense Tracker API  →  http://localhost:5000")
    print("   Run serve.py in another terminal, then open http://localhost:8000")
    app.run(debug=True, port=5000)
