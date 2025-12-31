# =========================
# google_integration.py
# =========================

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar"
]

TOKEN_FILE = "token.pickle"


def get_google_services():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    gmail_service = build("gmail", "v1", credentials=creds)
    calendar_service = build("calendar", "v3", credentials=creds)

    return gmail_service, calendar_service

import base64
from email.mime.text import MIMEText


def send_gmail(to, subject, body):
    gmail_service, _ = get_google_services()

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    gmail_service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

from datetime import datetime, timedelta


from datetime import datetime, timedelta
import pytz


def create_calendar_invite(title, attendee_emails):
    _, calendar_service = get_google_services()

    timezone = "Asia/Kolkata"
    tz = pytz.timezone(timezone)

    start = datetime.now(tz) + timedelta(days=1)
    end = start + timedelta(hours=1)

    event = {
        "summary": title,
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": timezone
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": timezone
        },
        "attendees": [
            {"email": email} for email in attendee_emails
        ],
    }

    calendar_service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates="all"
    ).execute()




