import requests
from google.adk.agents import Agent

def get_next_launch(_: str = "") -> dict:
    """
    Retrieves the next upcoming SpaceX launch.
    """
    try:
        response = requests.get("https://api.spacexdata.com/v5/launches/upcoming")
        response.raise_for_status()
        launches = response.json()
        if not launches:
            return {"status": "error", "error_message": "No upcoming launches found."}

        # Get the soonest launch
        next_launch = sorted(launches, key=lambda x: x["date_utc"])[0]
        launchpad = next_launch.get("launchpad", "")
        name = next_launch.get("name", "")
        date = next_launch.get("date_utc", "")

        # Fetch launchpad details
        pad_data = requests.get(f"https://api.spacexdata.com/v5/launchpads/{launchpad}").json()
        location = pad_data.get("locality", "Unknown Location")

        return {
            "status": "success",
            "report": {
                "launch_name": name,
                "launch_date": date,
                "location": location
            }
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

spacex_agent = Agent(
    name="spacex_agent",
    model="gemini-1.5-flash",
    description="Fetches information about the next SpaceX launch.",
    instruction="Return next SpaceX launch with name, date, and location.",
    tools=[get_next_launch],
)
