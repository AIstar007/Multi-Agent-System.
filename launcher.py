from google.adk.runtime import Runtime
from agents.planner_agent import PlannerAgent
from agents.spacex_agent import SpaceXAgent
from agents.weather_agent import WeatherAgent
from agents.delay_agent import DelayAgent

if __name__ == "__main__":
    runtime = Runtime()

    # Register all agents
    runtime.add_agent(PlannerAgent())
    runtime.add_agent(SpaceXAgent())
    runtime.add_agent(WeatherAgent())
    runtime.add_agent(DelayAgent())

    # Start the multi-agent system
    runtime.run()