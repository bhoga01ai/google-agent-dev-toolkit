import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

# AGENT Deployment 
from vertexai import agent_engines
from vertexai.preview.reasoning_engines import AdkApp
import os
# IMPORT the agent
from teaching_assistant_agent.agent import root_agent

# init vertexai

import vertexai
vertexai.init(
    project=os.getenv("GOOGLE_PROJECT_ID"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket=os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
)

# Create Agent Engine APP

adk_app = AdkApp(agent=root_agent,
                  enable_tracing=True
                )

my_remote_agent = agent_engines.create(
    adk_app,
    display_name="my_teaching_assistant_agent",
    requirements=[
        "google-adk>=1.0.0",
        "google-cloud-aiplatform[agent_engines]",
        "google-genai",
        "pydantic",
        "absl-py"
    ]
)
print(f"Created remote agent: {my_remote_agent.resource_name}")