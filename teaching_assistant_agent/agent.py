# STEPS  
# STEP 1: import API KEYS
# STEP 2. Import libraries
# STEP 3. Define the agent
    # 1. Add a model
    # 2. Add a name
    # 3. Add an instruction
    # 4. Add tools
    # 5. Add a description
# STEP 4. Run the agent using adk web tool (for development)
# STEP 5. Deploy the agent using Vertex Agent Engine (for production)

from dotenv import load_dotenv
load_dotenv()
from . import prompt

from google.adk import Agent
from google.adk.tools import google_search
# from google.adk.tools import FunctionTool

# def get_weather(location: str) -> str:
#     """Get the current weather in a given location"""
#     return "20 degrees"

# def get_current_time() -> str:
#     """Get the current time"""
#     return "10:00 AM"

MODEL="gemini-2.0-flash"

root_agent=Agent(
    model=MODEL,
    name="teaching_assistant_agent",
    instruction=prompt.TEACHING_ASSISTANT_PROMPT,
    # tools=[FunctionTool(get_weather), FunctionTool(get_current_time)],
    tools=[google_search],
    description="Agent to assist students to plan and learn any skills that they want to learn. "   # purpose of the agent
)