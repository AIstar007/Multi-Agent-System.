import os
import json
import csv
import markdown2
from dotenv import load_dotenv
from datetime import datetime
from time import time
from weasyprint import HTML
from google.adk.runtime import Runtime
from google.adk.messages import Goal

# Import ADK-compatible agents
from agents.planner_agent import PlannerAgent
from agents.spacex_agent import SpaceXAgent
from agents.weather_agent import WeatherAgent
from agents.delay_agent import DelayAgent

# Load environment variables from .env
load_dotenv()

# Set folders
EVAL_FOLDER = "evals"
RESULT_FOLDER = "results"
os.makedirs(RESULT_FOLDER, exist_ok=True)

# Initialize report content
md_lines = ["# 🧪 Multi-Agent System Evaluation Report\n"]
csv_rows = [["Test ID", "Status", "Details", "Timestamp", "Runtime (s)"]]

def evaluate_case(test_file):
    test_path = os.path.join(EVAL_FOLDER, test_file)

    # Read test case JSON using UTF-8 encoding
    with open(test_path, 'r', encoding='utf-8') as f:
        case = json.load(f)

    print(f"\n▶️ Running test: {case['test_id']}")
    start_time = time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Set up ADK runtime and agents
    runtime = Runtime()
    runtime.add_agent(PlannerAgent())
    runtime.add_agent(SpaceXAgent())
    runtime.add_agent(WeatherAgent())
    runtime.add_agent(DelayAgent())

    result_container = {}

    try:
        runtime.run([
            Goal(name="user_goal", value=case["input_goal"], to="planner")
        ])

        # Extract latest result (assuming DelayAgent or final agent stores output)
        delay_agent = runtime.get_agent("delay")
        result = getattr(delay_agent, "latest_result", {})
        assessment = getattr(delay_agent, "latest_assessment", None)

    except Exception as e:
        runtime_duration = round(time() - start_time, 2)
        status = "FAIL"
        details = [f"Exception: {str(e)}"]

        # Log error in reports
        md_lines.extend([
            f"## ❌ {case['test_id']} - {status}",
            f"**Input Goal:** {case['input_goal']}",
            f"**Exception:** `{str(e)}`",
            f"**Timestamp:** {timestamp}",
            f"**Runtime:** {runtime_duration} seconds",
            "---\n"
        ])
        csv_rows.append([case["test_id"], status, "; ".join(details), timestamp, runtime_duration])
        return

    # Default PASS
    status = "PASS"
    details = []

    # Check expected result keys
    for key in case.get("expected_result_keys", []):
        if key not in result:
            status = "FAIL"
            details.append(f"Missing key: {key}")

    # Validate assessment
    if assessment and case.get("valid_assessments"):
        if assessment not in case["valid_assessments"]:
            status = "FAIL"
            details.append(f"Unexpected assessment: {assessment}")

    runtime_duration = round(time() - start_time, 2)

    # Append to Markdown report
    md_lines.extend([
        f"## {'✅' if status == 'PASS' else '❌'} {case['test_id']} - {status}",
        f"**Input Goal:** {case['input_goal']}",
        f"**Timestamp:** {timestamp}",
        f"**Runtime:** {runtime_duration} seconds",
        f"**Result:**\n```json\n{json.dumps(result, indent=2)}\n```",
        f"**Details:** {', '.join(details) if details else 'All checks passed.'}",
        "\n---\n"
    ])

    # Append to CSV
    csv_rows.append([
        case["test_id"],
        status,
        "; ".join(details) if details else "All checks passed.",
        timestamp,
        runtime_duration
    ])

# Run all tests in /evals
test_files = [f for f in os.listdir(EVAL_FOLDER) if f.endswith(".json")]
for tf in test_files:
    evaluate_case(tf)

# Write Markdown report
md_report_path = os.path.join(RESULT_FOLDER, "eval_report.md")
with open(md_report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

# Write CSV report
csv_report_path = os.path.join(RESULT_FOLDER, "eval_report.csv")
with open(csv_report_path, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csv_rows)

# Convert Markdown to PDF
pdf_report_path = os.path.join(RESULT_FOLDER, "eval_report.pdf")
md_html = markdown2.markdown("\n".join(md_lines))
HTML(string=md_html).write_pdf(pdf_report_path)

# Done!
print("\n✅ Evaluation complete.")
print(f"📄 Markdown Report: {md_report_path}")
print(f"📊 CSV Report: {csv_report_path}")
print(f"🧾 PDF Report: {pdf_report_path}")