# =========================
# manager_agent.py
# =========================

from google_integration import send_gmail

class ManagerAgent:

    def request_approval(self, employee_name, manager_email, employee_email):
        approve_link = (
            f"http://localhost:8000/approve"
            f"?employee_name={employee_name}"
            f"&manager_email={manager_email}"
            f"&employee_email={employee_email}"
        )

        send_gmail(
            to=manager_email,
            subject="Approval Required: Employee Onboarding",
            body=(
                f"Please approve onboarding for {employee_name}.\n\n"
                f"Click here to approve:\n{approve_link}"
            )
        )
