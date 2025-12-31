# =========================
# app.py
# =========================

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from agent import HROnboardingAgent
from learning_agent import LearningCoachAgent
from auth import authenticate, require_login

app = FastAPI(title="Agentic AI – HR & L&D System")

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)

templates = Jinja2Templates(directory="templates")


# -------------------------
# LOGIN
# -------------------------
@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    if authenticate(email, password):
        request.session["user"] = email
        return RedirectResponse("/dashboard", status_code=302)

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid credentials"}
    )


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)


# -------------------------
# DASHBOARD
# -------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    auth = require_login(request)
    if auth:
        return auth

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


# -------------------------
# AGENT ACTIONS
# -------------------------
@app.post("/onboard-ui")
def onboard_ui(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    manager_name: str = Form(...),
    manager_email: str = Form(...)
):
    auth = require_login(request)
    if auth:
        return auth

    agent = HROnboardingAgent(
        {
            "name": name,
            "email": email,
            "manager_name": manager_name,
            "manager_email": manager_email
        }
    )

    agent.run()

    return RedirectResponse("/dashboard", status_code=302)


@app.post("/learning-ui")
def learning_ui(
    request: Request,
    role: str = Form(...),
    current_skills: str = Form(...),
    target_skills: str = Form(...)
):
    auth = require_login(request)
    if auth:
        return auth

    coach = LearningCoachAgent(
        {
            "role": role,
            "current_skills": current_skills,
            "target_skills": target_skills
        }
    )

    plan = coach.generate_learning_plan()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "learning_plan": plan
        }
    )
from google_integration import create_calendar_invite
from tools import complete_onboarding

@app.get("/approve")
def approve_onboarding(
    employee_name: str,
    manager_email: str
):
    # ⚠️ In real product, fetch details from DB
    # For now, we simulate using manager email as attendee

    create_calendar_invite(
        title=f"Intro Meeting: {employee_name}",
        attendee_emails=[manager_email]
    )
    from google_integration import send_gmail

    send_gmail(
        to=manager_email,
        subject="Employee Onboarding Completed",
        body=f"Onboarding for {employee_name} has been approved and scheduled."
    )


    complete_onboarding(employee_name)

    return {
        "status": "approved",
        "message": f"Onboarding approved for {employee_name}"
    }
