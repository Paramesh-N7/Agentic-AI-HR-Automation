# =========================
# auth.py
# =========================

from fastapi import Request
from fastapi.responses import RedirectResponse

# TEMP users (replace with DB later)
USERS = {
    "admin@company.com": "test123"
}

def authenticate(email: str, password: str) -> bool:
    return USERS.get(email) == password


def require_login(request: Request):
    if not request.session.get("user"):
        return RedirectResponse("/", status_code=302)
