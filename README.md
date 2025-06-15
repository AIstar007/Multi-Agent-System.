# 🤖 Multi-Agent AI System using Google ADK

This project implements a **multi-agent system** inspired by Google ADK. It takes a **user goal**, creates a **dynamic agent plan**, and routes data through a pipeline of **modular agents**, each enriching the results of the previous agent until the goal is fulfilled. Includes a full evaluation suite, visual dashboard, and email reporting.

---

## 🚀 Example Goal

```
"Find the next SpaceX launch, check weather at that location, then summarize if it may be delayed."
```

---

## 🧠 Agent Pipeline

1. **Planner Agent**: Interprets the user goal and defines a workflow.
2. **SpaceX Agent**: Fetches data on the next launch.
3. **Weather Agent**: Gets weather for the launch location.
4. **Delay Agent**: Assesses if the weather could delay the launch.

---

## 🧰 Built With

- **Python 3.10+**
- [OpenWeatherMap API](https://openweathermap.org/api)
- [SpaceX Launches API](https://github.com/r-spacex/SpaceX-API)
- `streamlit` – for live dashboards
- `dotenv` – for managing secrets
- `markdown2`, `weasyprint` – for markdown to PDF reports
- `smtplib`, `email` – for sending results via email

---

## 🧩 Project Structure

```
multi-agent-system/
│
├── agents/              # Modular agents
│   ├── planner_agent.py
│   ├── spacex_agent.py
│   ├── weather_agent.py
│   └── delay_agent.py
│
├── core/                # Agent pipeline execution logic
│   └── agent_manager.py
│
├── evals/               # Test cases (JSON format)
│   ├── test_case_1.json
    ├── test_case_2.json
│   └── test_spacex.json
│
├── results/             # Evaluation outputs
│   ├── eval_report.csv
│   ├── eval_report.md
│   └── eval_report.pdf
│
├── .env                 # API keys and credentials (NOT committed)
├── run.py               # CLI: run single user goal
├── eval_runner.py       # Batch test runner & report generator
├── eval_viewer.py       # Streamlit dashboard evaluator
├── email_report.py      # Email the final report
├── requirements.txt     # All dependencies
└── README.md            # This file
```

---

## 🔐 .env Setup

```dotenv
GOOGLE_API_KEY=your_GOOGLE_API_KEY
GOOGLE_GENAI_USE_VERTEXAI="FALSE"

OPENWEATHER_API_KEY=your_openweather_api_key

SPACEX_API_URL=https://api.spacexdata.com/v5/launches/latest

EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECEIVER=receiver@example.com

OTEL_SERVICE_NAME=multi_agent_system
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf

ENABLE_TRACING=true
```

---

## 🛠️ Installation

```bash
git clone https://github.com/yourusername/multi-agent-system.git
cd multi-agent-system
pip install -r requirements.txt
cp .env.example .env  # Fill in your credentials
```

---

## ▶️ Running the System

### 🔹 CLI Mode

```bash
adk web
```

### 🔹 Evaluate All Test Cases

```bash
python eval_runner.py
```

### 🔹 Launch the Streamlit Dashboard

```bash
streamlit run eval_viewer.py
```

Features:
- Filter test cases by status or keyword
- View charts (pass/fail rate, runtime)
- Re-run selected tests
- Export filtered reports (Markdown, PDF, CSV, JSON)

---

## 📧 Send Report by Email

```bash
python email_report.py
```

---

## 📈 Evaluation Output

All reports are saved to the `/results` folder:

- 📄 `eval_report.md` — Human-readable summary
- 📊 `eval_report.csv` — Raw data for tracking
- 🧾 `eval_report.pdf` — Shareable PDF report
- 🖼️ Charts — via `eval_viewer.py`

---

## ✨ Features

- ✅ Modular agent design
- ✅ API chaining with dependency passing
- ✅ Auto-evaluation against test cases
- ✅ Real-time Streamlit dashboard
- ✅ PDF/CSV/Markdown report generation
- ✅ Optional email report delivery

---

## 🔐 Security Notes

- DO NOT commit your `.env` file.
- Use **App Passwords** (e.g., for Gmail) instead of your main password.

---

## 🧪 Sample Test Case Format

```json
{
  "test_id": "test_case_1",
  "input_goal": "Find the next SpaceX launch, check weather at that location, then summarize if it may be delayed.",
  "expected_plan": ["spacex", "weather", "delay"],
  "expected_result_keys": ["launch", "weather", "assessment"],
  "valid_assessments": [
    "✅ Launch is likely to proceed as planned.",
    "⚠️ Possible delay due to bad weather."
  ]
}

{
  "test_id": "test_case_2",
  "input_goal": "Get next launch and check delay conditions using weather",
  "expected_plan": ["spacex", "weather", "delay"],
  "expected_result_keys": ["launch", "weather", "assessment"],
  "valid_assessments": [
    "✅ Launch is likely to proceed as planned.",
    "⚠️ Possible delay due to bad weather."
  ]
}

{
  "test_id": "spacex-weather-delay-test",
  "input_goal": "Find the next SpaceX launch, check weather at that location, then summarize if it may be delayed.",
  "expected_result_keys": ["launch_location", "weather_forecast", "assessment"],
  "valid_assessments": ["Likely delayed", "On schedule", "Possibly delayed"]
}
```


---

## 🤝 Contribution

Pull requests welcome! If you want to add more agents, APIs, or evaluation metrics, feel free to open an issue.

---
