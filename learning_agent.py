# =========================
# learning_agent.py
# =========================

import os
from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


llm = ChatOpenAI(
    temperature=0.3,
    api_key=os.getenv("OPENAI_API_KEY")
)

PROMPT = """
You are an AI Learning & Development Coach.

Your task:
Create a personalized learning plan for an employee.

Employee details:
Role: {role}
Current Skills: {current_skills}
Target Skills: {target_skills}

Instructions:
1. Identify skill gaps
2. Recommend learning focus areas
3. Create a 4-week learning plan
4. Use simple, practical language

Return the response in structured bullet points.
"""


class LearningCoachAgent:

    def __init__(self, employee_profile: dict):
        self.profile = employee_profile

    def generate_learning_plan(self):

        prompt = PromptTemplate(
            input_variables=["role", "current_skills", "target_skills"],
            template=PROMPT
        )

        response = llm.invoke(
            prompt.format(**self.profile)
        )

        return response.content
