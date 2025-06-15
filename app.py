import streamlit as st
from dotenv import load_dotenv
from types import AgentTask
from core.agent_manager import ADKAgentManager
from tracing import on_task_start, on_task_complete
from logging import trace_event
from google.adk.registry import register_agent
import json

# Load environment variables
load_dotenv()

# Initialize ADK manager
manager = ADKAgentManager()

# Explicitly register agents (optional if auto-registered elsewhere)
# from agents.spacex_agent import SpaceXAgent
# from agents.weather_agent import WeatherAgent
# from agents.delay_agent import DelayAgent
# manager.register("spacex", SpaceXAgent())
# manager.register("weather", WeatherAgent())
# manager.register("delay", DelayAgent())

# Streamlit UI Setup
st.set_page_config(page_title="🛰️ SpaceX Launch Checker", layout="centered")

st.title("🛰️ SpaceX Launch & Delay Predictor")
st.markdown("Enter a goal like: `Find next SpaceX launch, check weather, and tell if it may be delayed.`")

goal = st.text_input("Enter your goal:")

# Session state cache
if "cached_result" not in st.session_state:
    st.session_state.cached_result = None

if st.button("Run Agents") and goal:
    with st.spinner("Working on it..."):
        try:
            # Create ADK-compatible task
            task = AgentTask(input=goal)

            # Observability: hook before start
            on_task_start(task)
            trace_event("TaskStarted", {"goal": goal})

            # Route the task through the ADK system
            response = manager.route_task(task)

            # Observability: hook after completion
            on_task_complete(task, response)
            trace_event("TaskCompleted", {"output": response.output})

            result = response.output
            st.session_state.cached_result = result  # Cache result

            st.success("✅ Goal Processed!")

            st.markdown("### 🧠 Breakdown")
            for k, v in result.items():
                st.markdown(f"**🔹 {k.capitalize()}:**")
                st.code(json.dumps(v, indent=2), language="json")

            st.markdown("### 🔍 Summary")
            st.markdown(f"**🚀 Launch:** {result['launch']['name']}")
            st.markdown(f"**🕒 Launch Time:** {result['launch']['launch_time']}")
            st.markdown(f"**📊 Weather:** {result['weather']['weather'][0]['description']}")
            st.markdown(f"**💡 Assessment:** {result['assessment']}")

        except Exception as e:
            trace_event("TaskError", {"error": str(e)})
            st.error(f"❌ Something went wrong: {e}")

# Show cached result if exists
if st.session_state.cached_result:
    with st.expander("📦 Cached Result"):
        st.json(st.session_state.cached_result)