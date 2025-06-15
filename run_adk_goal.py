from google.adk.runtime import Runtime
from google.adk.messages import Goal
from agents.planner_agent import PlannerAgent
from agents.spacex_agent import SpaceXAgent
from agents.weather_agent import WeatherAgent
from agents.delay_agent import DelayAgent

if __name__ == "__main__":
    runtime = Runtime()

    # Register agents
    runtime.add_agent(PlannerAgent())
    runtime.add_agent(SpaceXAgent())
    runtime.add_agent(WeatherAgent())
    runtime.add_agent(DelayAgent())

    # Send initial goal
    runtime.run([Goal(name="user_goal", value="Find the next SpaceX launch, check weather, and summarize if it may be delayed", to="planner")])