import json
import os
from datetime import datetime

# Anchor all data files to the directory where this script lives,
# so they work no matter what the working directory is when you
# start Flask or serve.py.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE  = os.path.join(_BASE_DIR, "user_data.json")
USER_FILE  = os.path.join(_BASE_DIR, "users.json")


def load_user_data(username):
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)
        value = all_data.get(username)
        # Guard against null / corrupt entries left in the JSON file
        return value if isinstance(value, dict) else None
    except (json.JSONDecodeError, IOError):
        return None


def save_user_data(username, data):
    all_data = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                all_data = json.load(f)
        except (json.JSONDecodeError, IOError):
            all_data = {}
    all_data[username] = data
    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f, indent=2)


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")
