from agents import delay_agent

def test_assess_delay():
    mock_weather = {
        "weather": [{"main": "Thunderstorm", "description": "heavy rain"}]
    }
    result = delay_agent.assess_delay(mock_weather)
    assert "delay" in result.lower()
    print("✅ Delay logic passed!")

if __name__ == "__main__":
    test_assess_delay()
