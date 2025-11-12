import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# AGENT Deployment 
from vertexai import agent_engines

# init vertexai

import vertexai
vertexai.init(
    project=os.getenv("GOOGLE_PROJECT_ID"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
)

# Create remote Agent Engine APP
remote_agent = vertexai.agent_engines.get('projects/278955585844/locations/us-central1/reasoningEngines/8184764557164544')
print(f"Found agent with resource ID: {remote_agent.resource_name}")
user_id = "123"
session = remote_agent.create_session(user_id=user_id)   
print(f"Created session for user ID: {user_id}")
print("Type 'quit' to exit.")

while True:
    user_input = input("Input: ")
    if user_input == "quit":
        break
    for event in remote_agent.stream_query(
        user_id=user_id, 
        session_id=session["id"],
        message=user_input
    ):
        if "content" in event:
            if "parts" in event["content"]:
                parts = event["content"]["parts"]
                for part in parts:
                    if "text" in part:
                        text_part = part["text"]
                        print(f"Response: {text_part}")
remote_agent.delete_session(user_id=user_id, session_id=session["id"])
print(f"Deleted session for user ID: {user_id}")