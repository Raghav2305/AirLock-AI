# streamlit_ui/dashboard.py

import os
import time
import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime, timedelta

# 🔗 Log file
LOG_FILE = os.path.join("logs", "blocked_prompts.log")

# 🌑 Page config
st.set_page_config(
    page_title="🛡️ Airlock AI - Blocked Prompts Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🚀 Header
st.markdown(
    """
    <style>
        .main-title {
            font-size: 3rem;
            font-weight: 800;
            text-align: center;
            color: #00f5d4;
            margin-bottom: 0.5rem;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #ccc;
            margin-bottom: 2rem;
        }
        .log-box {
            background-color: #111;
            border-left: 5px solid #ff4c4c;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 0.5rem;
            color: #eee;
        }
    </style>
    <div class='main-title'>🛡️ Airlock AI</div>
    <div class='subtitle'>Real-Time Monitoring of Blocked Prompts</div>
    """,
    unsafe_allow_html=True
)

# 🕹️ Sidebar Filters
st.sidebar.header("🔍 Filters")
refresh_interval = st.sidebar.slider("⏱ Auto-refresh (seconds)", 0, 60, 0)

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

search_input = st.sidebar.text_input("🔎 Search keyword", value=st.session_state.search_query)
st.session_state.search_query = search_input
search_query = st.session_state.search_query
days_filter = st.sidebar.slider("🗓️ Show logs from last N days", 1, 30, 7)

# 🔄 Auto-refresh
if refresh_interval > 0:
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = time.time()
    elif time.time() - st.session_state.last_refresh > refresh_interval:
        st.session_state.last_refresh = time.time()
        st.rerun()

# 🧠 Log parser
def load_logs():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    logs = []
    for line in lines:
        if "] 🚫 BLOCKED PROMPT:" in line:
            timestamp_str, prompt = line.split("] 🚫 BLOCKED PROMPT: ")
            timestamp_str = timestamp_str.strip("[ ")
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            logs.append({"timestamp": timestamp, "prompt": prompt.strip()})
    return logs

all_logs = load_logs()

# 🧼 Apply filters
filtered_logs = [
    log for log in all_logs
    if log["timestamp"] >= datetime.now() - timedelta(days=days_filter)
    and (search_query.lower() in log["prompt"].lower() if search_query else True)
]

# 📈 Chart for Blocked Prompts by Day
if filtered_logs:
    df = pd.DataFrame(filtered_logs)
    df["date"] = df["timestamp"].dt.date
    daily_counts = df.groupby("date").size().reset_index(name="Blocked Prompts")

    bar_chart = (
        alt.Chart(daily_counts)
        .mark_bar(color="#ff4c4c")
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("Blocked Prompts:Q"),
            tooltip=["date", "Blocked Prompts"]
        )
        .properties(
            title="📊 Blocked Prompts Over Time",
            width="container",
            height=300,
        )
    )
    st.altair_chart(bar_chart, use_container_width=True)

# 📊 Metrics
col1, col2 = st.columns(2)
col1.metric("🚫 Total Blocked Prompts", len(filtered_logs))
if filtered_logs:
    col2.metric("🕒 Last Blocked At", filtered_logs[-1]["timestamp"].strftime("%b %d, %Y %H:%M:%S"))
else:
    col2.metric("🕒 Last Blocked At", "N/A")

# 📋 Prompt Logs
st.markdown("---")
st.subheader("📄 Blocked Prompts")
if not filtered_logs:
    st.warning("No blocked prompts match your filters.")
else:
    for log in reversed(filtered_logs):
        st.markdown(
            f"""
            <div class="log-box">
                <strong>🕒 {log['timestamp'].strftime('%b %d, %Y %H:%M:%S')}</strong><br/>
                {log['prompt']}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")
st.caption("Airlock AI • Securing LLMs since 2025 🚀")
