import streamlit as st
import pandas as pd
import os
import subprocess
import matplotlib.pyplot as plt
import json
from datetime import datetime

from google.adk.runtime import Runtime
from google.adk.logging_utils import init_logger

st.set_page_config(page_title="🧠 ADK Evaluation Dashboard", layout="wide")

EVAL_FOLDER = "evals"
RESULT_CSV = "results/eval_report.csv"
RESULT_MD = "results/eval_report.md"
RESULT_PDF = "results/eval_report.pdf"

st.title("🧠 Google ADK - Multi-Agent Evaluation Dashboard")
st.markdown("Visual insights into your ADK-compliant system's performance.")

with st.sidebar:
    st.header("🔍 Filters")
    status_filter = st.multiselect("Status", ["PASS", "FAIL"], default=["PASS", "FAIL"])
    keyword = st.text_input("Search Test ID or Details")

    st.markdown("---")
    st.markdown("📅 Download Reports")
    if os.path.exists(RESULT_MD):
        st.download_button("⬇️ Markdown", open(RESULT_MD, "rb"), file_name="eval_report.md")
    if os.path.exists(RESULT_PDF):
        st.download_button("⬇️ PDF", open(RESULT_PDF, "rb"), file_name="eval_report.pdf")

    st.markdown("---")
    st.header("📡 Upload New ADK Test Case")
    uploaded_file = st.file_uploader("Upload JSON ADK Test Case", type="json")
    if uploaded_file is not None:
        try:
            new_test = json.load(uploaded_file)
            test_id = new_test.get("test_id", f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            save_path = os.path.join(EVAL_FOLDER, f"{test_id}.json")
            with open(save_path, "w") as f:
                json.dump(new_test, f, indent=2)
            st.success(f"✅ Uploaded as {test_id}.json")
        except Exception as e:
            st.error(f"Invalid JSON: {e}")

    st.markdown("---")
    st.header("🔁 Auto Evaluation")
    auto_run = st.checkbox("Enable Auto Re-run")
    interval = st.slider("Re-run Interval (minutes)", 1, 30, 5)
    if auto_run:
        if "last_run" not in st.session_state:
            st.session_state.last_run = datetime.now()

        elapsed_minutes = (datetime.now() - st.session_state.last_run).seconds / 60
        if elapsed_minutes > interval:
            with st.spinner("Auto re-running `eval_runner.py`..."):
                subprocess.run(["python", "eval_runner.py"])
                st.session_state.last_run = datetime.now()
            st.success("✅ Auto evaluation completed.")

if st.button("🔁 Re-run Evaluation Now"):
    with st.spinner("Running `eval_runner.py`..."):
        subprocess.run(["python", "eval_runner.py"])
    st.success("✅ Evaluation completed.")

if not os.path.exists(RESULT_CSV):
    st.warning("⚠️ No evaluation results found. Run `eval_runner.py` first.")
    st.stop()

# Load ADK-compatible evaluation report
df = pd.read_csv(RESULT_CSV)
df_filtered = df[df["Status"].isin(status_filter)]

if keyword:
    df_filtered = df_filtered[df_filtered["Test ID"].str.contains(keyword, case=False) |
                               df_filtered["Details"].str.contains(keyword, case=False)]

st.markdown(f"### ✅ Showing {len(df_filtered)} Test Case(s)")

st.markdown("### 📊 Pass/Fail Summary")
status_counts = df["Status"].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
ax1.axis("equal")
st.pyplot(fig1)

st.markdown("### ⏱ Runtime Distribution (seconds)")
fig2, ax2 = plt.subplots()
df["Runtime (s)"].hist(ax=ax2, bins=10, color="skyblue", edgecolor="black")
ax2.set_xlabel("Runtime (seconds)")
ax2.set_ylabel("Frequency")
st.pyplot(fig2)

st.markdown("### 📋 Evaluation Details")
st.dataframe(df_filtered, use_container_width=True)

st.markdown("---")
for _, row in df_filtered.iterrows():
    with st.expander(f"🧪 {row['Test ID']} — {row['Status']}"):
        st.markdown(f"**🕒 Timestamp:** `{row['Timestamp']}`")
        st.markdown(f"**⏱ Runtime:** `{row['Runtime (s)']}s`")
        st.markdown(f"**📄 Details:** {row['Details']}")

st.markdown("### 📄 Export Filtered ADK Test Set")
if st.button("Download JSON Batch of Filtered Tests"):
    test_ids = df_filtered["Test ID"].tolist()
    json_tests = []

    for tid in test_ids:
        test_file_path = os.path.join(EVAL_FOLDER, f"{tid}.json")
        if os.path.exists(test_file_path):
            with open(test_file_path, "r") as f:
                test = json.load(f)
                json_tests.append(test)

    export_path = "results/filtered_tests_export.json"
    with open(export_path, "w") as f:
        json.dump(json_tests, f, indent=2)

    st.download_button("⬇️ Download JSON", open(export_path, "rb"), file_name="filtered_tests.json")