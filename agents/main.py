import os
from dotenv import load_dotenv
from planner_agent.agent import planner_agent
from spacex_agent.agent import spacex_agent, fetch_next_launch
from weather_agent.agent import weather_agent, get_weather_at_location
from summary_agent.agent import summary_agent, summarize_launch_status

# Load API Keys from .env
load_dotenv()

def main():
    # Step 1: Get user goal
    user_goal = "Find the next SpaceX launch, check weather at that location, then summarize if it may be delayed."

    # Step 2: Planner decides agent sequence
    plan_result = planner_agent.run(user_goal)
    print("\n🧠 Planner Result:\n", plan_result.get("result", ""))

    # Step 3: SpaceX Agent fetches next launch
    spacex_result = fetch_next_launch()
    if spacex_result["status"] != "success":
        print("❌ SpaceX Agent Error:", spacex_result["error_message"])
        return

    print("\n🚀 SpaceX Launch Data:\n", spacex_result["launch"])

    # Step 4: Weather Agent uses launch site info
    location = spacex_result["launch"]["location"]
    weather_result = get_weather_at_location(location)
    if weather_result["status"] != "success":
        print("❌ Weather Agent Error:", weather_result["error_message"])
        return

    print("\n🌦️ Weather Report:\n", weather_result["report"])

    # Step 5: Summary Agent combines results
    data_for_summary = {
        "launch_data": spacex_result["launch"],
        "weather_data": weather_result,
    }

    summary_result = summarize_launch_status(data_for_summary)
    if summary_result["status"] == "success":
        print("\n📋 Final Summary:\n", summary_result["summary"])
    else:
        print("❌ Summary Agent Error:", summary_result["error_message"])

if __name__ == "__main__":
    main()