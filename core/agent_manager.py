from agent_manager import AgentManager
# Update the import path to match your project structure or use a relative import if types.py is local
from types import AgentTask, AgentResponse
from google.adk.agents import planner_agent, spacex_agent, weather_agent, delay_agent

class ADKAgentManager(AgentManager):
    def route_task(self, task: AgentTask) -> AgentResponse:
        user_goal = task.input
        plan = planner_agent.plan(user_goal)
        context = {}

        for step in plan:
            if step == "spacex":
                context["launch"] = spacex_agent.get_next_launch()

            elif step == "weather":
                if "launch" not in context:
                    raise ValueError("Missing launch data before fetching weather.")
                coords = weather_agent.get_launchpad_coordinates(context["launch"]["launchpad_id"])
                context["weather"] = weather_agent.get_weather(*coords)

            elif step == "delay":
                if "weather" not in context:
                    raise ValueError("Missing weather data before delay assessment.")
                context["assessment"] = delay_agent.assess_delay(context["weather"])

        return AgentResponse(output=context)
