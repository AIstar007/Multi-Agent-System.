from google.adk.agents import Agent
from google.adk.schema import TaskOutput

def plan_route(goal: str) -> dict:
    """
    Plans which agents to call based on user goal.
    """
    if "launch" in goal.lower():
        return {
            "status": "success",
            "plan": ["spacex_agent", "weather_agent", "summary_agent"]
        }
    return {
        "status": "error",
        "error_message": "Cannot plan route for the given goal."
    }

planner_agent = Agent(
    name="planner_agent",
    model="gemini-1.5-flash",
    description="Decides agent sequence based on the user's goal",
    instruction="Route the task to agents in logical order based on goal.",
    tools=[plan_route],
)
