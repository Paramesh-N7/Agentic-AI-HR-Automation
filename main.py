import os
from dotenv import load_dotenv
from agent import HROnboardingAgent


employee_data = {
    "name": "employee",
    "email": "employee@company.com",
    "manager": "manager"
}

agent = HROnboardingAgent(employee_data)
agent.run()

from learning_agent import LearningCoachAgent

learning_profile = {
    "role": "Junior Software Engineer",
    "current_skills": "Python basics, HTML, SQL",
    "target_skills": "Advanced Python, APIs, System Design"
}

coach = LearningCoachAgent(learning_profile)
plan = coach.generate_learning_plan()

print("\n LEARNING PLAN\n")
print(plan)
