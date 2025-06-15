from dotenv import load_dotenv
from core.agent_manager import ADKAgentManager
from types import AgentTask
from core.tracing import setup_tracing  # 👈 Add tracing setup

load_dotenv()

# Setup OpenTelemetry Tracer
tracer = setup_tracing()  # 👈 Initialize tracer

if __name__ == "__main__":
    user_goal = "Find next SpaceX launch, check weather, and tell if it may be delayed."
    task = AgentTask(input=user_goal)
    manager = ADKAgentManager()

    # 👇 Trace the main ADK routing span
    with tracer.start_as_current_span("spaceX-mission"):
        response = manager.route_task(task)
        result = response.output

    # Output result as usual
    print("\n🚀 Launch:", result['launch']['name'])
    print("🕒 Launch Time:", result['launch']['launch_time'])
    print("📊 Weather:", result['weather']['weather'][0]['description'])
    print("💡 Assessment:", result['assessment'])