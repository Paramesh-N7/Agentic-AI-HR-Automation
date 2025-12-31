from google_integration import send_gmail, create_calendar_invite


def send_welcome_email(employee_name, employee_email):
    send_gmail(
        to=employee_email,
        subject="Welcome to the Company!",
        body=f"Hi {employee_name}, welcome aboard!"
    )
    return {"status": "success"}


def notify_manager(manager_name, manager_email, employee_name):
    send_gmail(
        to=manager_email,
        subject="Approval Required: Employee Onboarding",
        body=f"Please review and approve onboarding for {employee_name}."
    )

def complete_onboarding(employee_name):
    print(f"✅ Onboarding completed for {employee_name}")
    return {"status": "success"}
