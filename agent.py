# =========================
# agent.py
# =========================

import os
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from tools import (
    send_welcome_email,
    notify_manager
)

from manager_agent import ManagerAgent


# -------------------------
# Initialize LLM (Agent Brain)
# -------------------------
llm = ChatOpenAI(
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# -------------------------
# Agent Prompt (Policy)
# -------------------------
PROMPT = """
You are an HR onboarding AI agent.

Goal:
Onboard a new employee correctly.

Employee details:
Name: {name}
Email: {email}
Manager Name: {manager_name}
Manager Email: {manager_email}

Rules:
- If employee email is missing, do NOT send welcome email
- If manager name or email is missing, do NOT notify manager
- Always request manager approval at the end

Available actions:
- send_welcome_email
- notify_manager
- request_approval

Return actions as a comma-separated list in correct order.
"""

# =========================
# HR ONBOARDING AGENT
# =========================
class HROnboardingAgent:

    def __init__(self, employee: dict):
        self.employee = employee
        self.memory = []
        self.manager_agent = ManagerAgent()

    # -------------------------
    # THINK: Decide what to do
    # -------------------------
    def think(self):
        # ---- Schema validation ----
        required_keys = ["name", "email", "manager_name", "manager_email"]
        for key in required_keys:
            if key not in self.employee:
                raise ValueError(f"Missing required field: {key}")

        # ---- Build prompt ----
        prompt = PromptTemplate(
            input_variables=["name", "email", "manager_name", "manager_email"],
            template=PROMPT
        )

        response = llm.invoke(
            prompt.format(**self.employee)
        )

        raw_actions = [a.strip() for a in response.content.split(",")]

        validated_actions = []

        employee_email = self.employee.get("email")
        manager_name = self.employee.get("manager_name")
        manager_email = self.employee.get("manager_email")

        # ---- Safety enforcement ----
        for action in raw_actions:
            if action == "send_welcome_email" and not employee_email:
                continue
            if action == "notify_manager" and (not manager_name or not manager_email):
                continue
            validated_actions.append(action)

        return validated_actions

    # -------------------------
    # ACT: Execute actions
    # -------------------------
    def act(self, action: str):

        if action == "send_welcome_email":
            send_welcome_email(
                self.employee["name"],
                self.employee["email"]
            )
            return {"status": "done"}

        elif action == "notify_manager":
            notify_manager(
                self.employee["manager_name"],
                self.employee["manager_email"],
                self.employee["name"],
            )
            return {"status": "done"}

        elif action == "request_approval":
            self.manager_agent.request_approval(
                self.employee["name"],
                self.employee["manager_email"],
                self.employee["email"]
            )
            return {"status": "pending_approval"}


    # -------------------------
    # RUN: Agent lifecycle
    # -------------------------
    def run(self):
        print("\n HR Agent reasoning...\n")

        plan = self.think()

        for step in plan:
            print(f" HR Agent chose action: {step}")
            result = self.act(step)

            if result and result.get("status") == "pending_approval":
                self.memory.append("approval_requested")
                print("⏸ Waiting for manager approval...")
                break
            else:
                self.memory.append(step)

        print("\n Agent Memory:", self.memory)
