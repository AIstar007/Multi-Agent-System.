from google.adk.agents import Agent

def summarize_launch_status(data: dict) -> dict:
    """
    Combines SpaceX launch and weather data to produce a summary.
    Args:
        data (dict): Dictionary containing results from previous agents.
            {
                "launch_data": {...},
                "weather_data": {...}
            }
    Returns:
        dict: Summary report
    """
    try:
        launch = data.get("launch_data", {})
        weather = data.get("weather_data", {}).get("report", {})
        
        if not launch or not weather:
            return {
                "status": "error",
                "error_message": "Missing data for summary generation"
            }

        summary = (
            f"🚀 The next SpaceX launch is '{launch['name']}' "
            f"scheduled on {launch['date']} from {launch['location']}.\n\n"
            f"🌤️ Weather at the launch site: {weather['weather_condition']}, "
            f"{weather['temperature_celsius']}°C, Wind speed: {weather['wind_speed_mps']} m/s.\n"
        )

        # Simple delay risk heuristic
        if weather["wind_speed_mps"] > 10:
            summary += "\n⚠️ High wind speed may delay the launch."
        else:
            summary += "\n✅ Weather conditions look good for launch."

        return {"status": "success", "summary": summary}
    
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

summary_agent = Agent(
    name="summary_agent",
    model="gemini-1.5-flash",
    description="Generates final summary based on SpaceX and weather info.",
    instruction="Combine launch and weather data and check for delays.",
    tools=[summarize_launch_status],
)