from google.adk.runtime import AgentRuntime
from tracing import enable_tracing
import logging
import os
import sys
from dotenv import load_dotenv


load_dotenv()


# Optional: Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MultiAgentSystem")

def main():
    # Enable OpenTelemetry (Prometheus + Grafana compatible)
    enable_tracing(service_name="multi_agent_system")

    # Load agent runtime from adk.yaml
    runtime = AgentRuntime.from_yaml("adk.yaml")

    # Start the runtime (non-blocking by default)
    logger.info("🚀 Starting Agent Runtime...")
    runtime.start(block=True)

    # Optional: Send a test goal
    if len(sys.argv) > 1:
        goal_text = " ".join(sys.argv[1:])
        from adk.messages import Goal
        runtime.send_goal(Goal(name="user_goal", value=goal_text, to="planner"))

if __name__ == "__main__":
    main()