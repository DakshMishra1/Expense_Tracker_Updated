<div align="center">

<!-- HEADER BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=200&section=header&text=Expense%20Tracker&fontSize=60&fontColor=ffffff&fontAlignY=38&desc=Full-Stack%20Personal%20Finance%20Manager&descAlignY=60&descColor=a78bfa" width="100%"/>

<!-- BADGES -->
<p>
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-a78bfa?style=for-the-badge"/>
</p>

<p>
  <img src="https://img.shields.io/github/stars/DakshMishra1/Expense_Tracker_Updated?style=flat-square&color=a78bfa"/>
  <img src="https://img.shields.io/github/forks/DakshMishra1/Expense_Tracker_Updated?style=flat-square&color=7c3aed"/>
  <img src="https://img.shields.io/github/issues/DakshMishra1/Expense_Tracker_Updated?style=flat-square&color=ec4899"/>
  <img src="https://img.shields.io/github/last-commit/DakshMishra1/Expense_Tracker_Updated?style=flat-square&color=10b981"/>
</p>

<br/>

> **Track smarter. Spend wiser.**  
> A dual-interface (Web + CLI) expense manager with real-time analytics, budget enforcement, and a clean modular architecture — built for developers who care about design as much as functionality.

<br/>

[🚀 Live Demo](#) · [📖 Docs](#api-reference) · [🐛 Report Bug](https://github.com/DakshMishra1/Expense_Tracker_Updated/issues) · [💡 Request Feature](https://github.com/DakshMishra1/Expense_Tracker_Updated/issues)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Data Model](#data-model)
- [Security](#security)
- [Design Decisions](#design-decisions)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Author](#author)

---

## Overview

Expense Tracker is a full-stack personal finance application that gives you complete visibility into your spending — from a polished web dashboard to a terminal CLI. Unlike most expense tools that are UI-only wrappers, this project ships with a real REST API, session-based authentication, and a dual-interface design where both the web and CLI share the same underlying logic.

It's built to be **lightweight** (JSON storage, no database setup), **extensible** (clean module boundaries), and **honest** (real budget alerts, not just cosmetic indicators).

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      CLIENT LAYER                        │
│                                                          │
│   ┌──────────────────┐        ┌────────────────────┐    │
│   │   Web Browser    │        │   Terminal (CLI)    │    │
│   │  (localhost:8000)│        │    python Main.py   │    │
│   └────────┬─────────┘        └────────────┬───────┘    │
└────────────┼──────────────────────────────-┼────────────┘
             │                               │
             ▼                               │
┌────────────────────────┐                  │
│       serve.py         │  Static server   │
│     (Port :8000)       │  for frontend    │
└────────────┬───────────┘                  │
             │  HTTP / REST                 │ Direct calls
             ▼                               ▼
┌─────────────────────────────────────────────────────────┐
│                     API LAYER (Flask)                    │
│                       api.py :5000                       │
│                                                          │
│   /auth  /expenses  /limits  /spending  /data            │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER (utils.py)                 │
│         load_data()  save_data()  validate()             │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   JSON File Storage                      │
│              users.json   expenses.json                  │
└─────────────────────────────────────────────────────────┘
```

The system is deliberately split into two servers. `serve.py` handles static frontend delivery while `api.py` owns all business logic — mirroring how production systems separate concerns. Both the web app and CLI consume the same data layer, so behavior is consistent regardless of interface.

---

## Features

### Authentication System
- Register and login with hashed passwords (Werkzeug `generate_password_hash`)
- Session-based authentication with server-side state
- Protected routes — no data is accessible without a valid session

### Interactive Web Dashboard
- Summary cards: Total Budget / Spent / Remaining
- Doughnut chart — category-wise spending breakdown
- Bar chart — budget vs actual per category
- Recent transactions feed with timestamps

### Expense Management
- Add expenses with category, amount, and date
- Delete individual expenses by category and index
- Full transaction history view

### Budget Enforcement
- Set a global total budget limit
- Set per-category limits independently
- Smart real-time status indicators:
  - ✅ Within limit (< 80% used)
  - ⚠️ Near limit (80–99% used)
  - ❌ Over budget (> 100% used)

### Spending Analytics
- Category-wise spending summaries
- Remaining budget per category
- Aggregate totals across all categories

### CLI Interface
The terminal interface is not a stripped-down afterthought — it exposes the same feature set as the web app: adding expenses, viewing history, setting limits, and tracking spending. This makes the project genuinely dual-interface, not just "web app with a bonus script."

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.8+, Flask, Flask-CORS |
| Auth | Werkzeug Security (password hashing) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Charts | Chart.js |
| Storage | JSON flat files |
| CLI | Python (argparse / custom shell) |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/DakshMishra1/Expense_Tracker_Updated.git
cd Expense_Tracker_Updated

# 2. Install dependencies
pip install flask flask-cors werkzeug

# 3. Start the backend API
python api.py
# → Running on http://localhost:5000

# 4. In a separate terminal, start the frontend server
python serve.py
# → Serving on http://localhost:8000

# 5. Open the app
open http://localhost:8000
```

### CLI Mode

```bash
python Main.py
```

No additional setup required — the CLI uses the same data layer as the web app, so changes persist across both interfaces.

---

## API Reference

All endpoints are served from `http://localhost:5000`.

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/register` | Create a new user account |
| `POST` | `/api/login` | Authenticate and start a session |
| `POST` | `/api/logout` | Destroy the current session |
| `GET` | `/api/me` | Return current authenticated user |

### Expenses

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/expenses` | Add a new expense entry |
| `DELETE` | `/api/expenses/<category>/<index>` | Remove a specific expense |

### Budgets & Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/data` | Fetch all expense data for the session user |
| `PUT` | `/api/limits` | Update total or category-level budget limits |
| `GET` | `/api/spending` | Get category-wise spending summary |

### Example Request — Add Expense

```bash
curl -X POST http://localhost:5000/api/expenses \
  -H "Content-Type: application/json" \
  -d '{"category": "Food", "item": "Lunch", "amount": 150, "date": "2026-05-06"}'
```

### Example Response — Spending Summary

```json
{
  "Food": {
    "limit": 2000,
    "spent": 850,
    "remaining": 1150,
    "status": "within"
  },
  "Transport": {
    "limit": 500,
    "spent": 480,
    "remaining": 20,
    "status": "near"
  }
}
```

---

## Data Model

Each user's data is a JSON object keyed by category. The `Total Amount` key is reserved for the global budget.

```json
{
  "Total Amount": {
    "limit": 10000,
    "expenses": []
  },
  "Food": {
    "limit": 3000,
    "expenses": [
      {
        "item": "Dinner",
        "amount": 450,
        "date": "2026-05-04"
      },
      {
        "item": "Groceries",
        "amount": 800,
        "date": "2026-05-05"
      }
    ]
  },
  "Transport": {
    "limit": 1500,
    "expenses": [
      {
        "item": "Metro pass",
        "amount": 300,
        "date": "2026-05-01"
      }
    ]
  }
}
```

---

## Security

- Passwords are never stored in plaintext — Werkzeug's `generate_password_hash` / `check_password_hash` handles all credential storage
- Sessions are server-side — no sensitive data is held in the browser
- CORS is configured explicitly — only allowed origins can call the API

**Before deploying to production, change the Flask secret key:**

```python
# api.py
app.secret_key = "replace-this-with-a-long-random-string"
```

Generate a strong key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Design Decisions

### Why two servers instead of one?

Serving static files and handling API logic from the same process is common for small apps, but it creates coupling that makes both harder to reason about. Splitting `serve.py` (frontend delivery) from `api.py` (business logic) mirrors how real-world systems are structured — and makes it straightforward to later put a CDN in front of the frontend or containerize the API independently.

### Why JSON instead of a database?

For a project at this scale, JSON storage offers zero setup friction, human-readable debugging, and easy portability. The data layer is isolated in `utils.py`, meaning swapping to PostgreSQL or MongoDB is a contained change — not a rewrite. The abstraction is intentional.

### Why CLI + Web?

Most projects pick one interface and stop. Shipping both means the data layer had to be genuinely decoupled — you can't have hidden coupling when two completely different presentation layers consume the same logic. The CLI also makes the project more useful in environments where running a browser isn't convenient.

---

## Roadmap

- [ ] JWT-based stateless authentication
- [ ] PostgreSQL / MongoDB backend option
- [ ] CSV and PDF export for expense reports
- [ ] AI-powered spending insights and anomaly detection
- [ ] Cloud deployment (Docker + Railway/Render)
- [ ] Mobile app (React Native)
- [ ] Recurring expense tracking
- [ ] Multi-currency support

---

## Contributing

Contributions are welcome. To get started:

```bash
# 1. Fork the repo on GitHub

# 2. Clone your fork
git clone https://github.com/your-username/Expense_Tracker_Updated.git

# 3. Create a feature branch
git checkout -b feature/your-feature-name

# 4. Make your changes and commit
git commit -m "feat: add your feature description"

# 5. Push and open a Pull Request
git push origin feature/your-feature-name
```

Please follow conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`) and keep PRs focused on a single concern.

---

## Author

**Daksh Mishra**

[![GitHub](https://img.shields.io/badge/GitHub-DakshMishra1-181717?style=flat-square&logo=github)](https://github.com/DakshMishra1)

---

## License

This project is licensed under the [MIT License](LICENSE) — use it, fork it, build on it.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=100&section=footer" width="100%"/>

**If this project helped you, consider giving it a ⭐ — it means a lot.**

</div>
