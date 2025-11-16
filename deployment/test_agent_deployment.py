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

# Get the most recently deployed agent
agents_list = list(agent_engines.list())
if agents_list:
    remote_agent = agents_list[0]  # Get the first (most recent) agent
    client = agent_engines
    print(f"✅ Connected to deployed agent: {remote_agent.resource_name}")
else:
    print("❌ No agents found. Please deploy first.")

import asyncio

async def main():
    async for item in remote_agent.async_stream_query(
        message="what is an agent engine?",
        user_id="user_42",
    ):
        print(item['content']['parts'][0]['text'])

if __name__ == "__main__":
    asyncio.run(main())