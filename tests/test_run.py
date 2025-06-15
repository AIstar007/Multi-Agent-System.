import os
import logging
import time
from messages import Goal 
from runtime import AgentRuntime
from tracing import enable_tracing 
from google_api_tool_sets import calendar_tool_set 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)

def test_pipeline_with_google_api():
    enable_tracing(service_name="multi_agent_test_with_google_api")
    runtime = AgentRuntime.from_yaml("adk.yaml")
    runtime.start(block=False)
    time.sleep(2)

    # Configure the Google Calendar tool using your API key
    calendar_tool_set.configure_auth(client_id=None, client_secret=None, api_key=os.getenv("AIzaSyALMmjoazizRgx40Mnhrz2bbE2AZ4DS2KE"))

    # Send a goal that leverages the calendar tool — e.g. "What's on my calendar?"
    goal = Goal(name="user_goal", value="What are my next meetings?", to="planner")
    runtime.send_goal(goal)

    time.sleep(10)
    runtime.shutdown()
    print("✅ Pipeline run with Google Calendar tool completed!")

if __name__ == "__main__":
    test_pipeline_with_google_api()