# =========================
# integrations.py
# =========================

def send_email(to, subject, body):
    """
    Simulates sending an email.
    Replace this later with Gmail API.
    """
    print("EMAIL SENT")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    print("-" * 30)
    return True


def create_calendar_event(title, attendee):
    """
    Simulates calendar invite.
    Replace later with Google Calendar API.
    """
    print("CALENDAR EVENT CREATED")
    print(f"Title: {title}")
    print(f"Attendee: {attendee}")
    print("-" * 30)
    return True
