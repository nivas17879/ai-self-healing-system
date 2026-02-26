import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Self-Healing Maintenance System",
    layout="wide"
)

st.title("🧠 Intelligent Self‑Diagnosing Maintenance Dashboard")
st.write("Predictive • Diagnostic • Prescriptive AI System")
st.divider()

# =====================================
# LOAD MODEL & HISTORY
# =====================================

model = joblib.load("predictive_model.pkl")

log_file = "system_log.csv"

if os.path.exists(log_file):
    history = pd.read_csv(log_file)
else:
    history = pd.DataFrame(columns=[
        "Timestamp",
        "CPU", "Memory", "Error", "Response",
        "Threads",
        "Network_Traffic", "Disk_IO",
        "Crash_Probability", "Failure_Next_5min"
    ])

# =====================================
# INPUT SECTION
# =====================================

st.subheader("⚙️ System Parameters")

cpu = st.slider("CPU Usage (%)", 0, 100, 50)
memory = st.slider("Memory Usage (%)", 0, 100, 50)
error = st.slider("Error Rate", 0, 10, 1)
response = st.slider("Response Time (ms)", 0, 500, 200)
threads = st.slider("Active Threads", 0, 1000, 200)
network = st.slider("Network Traffic (MB/s)", 0, 1000, 100)
disk = st.slider("Disk I/O (MB/s)", 0, 500, 50)

# =====================================
# LIVE METRICS
# =====================================

st.subheader("📊 Live Metrics")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7 = st.columns(1)[0]

col1.metric("CPU Usage", f"{cpu}%")
col2.metric("Memory Usage", f"{memory}%")
col3.metric("Error Rate", error)

col4.metric("Response Time", f"{response} ms")
col5.metric("Network Traffic", f"{network} MB/s")
col6.metric("Disk I/O", f"{disk} MB/s")

col7.metric("Active Threads", threads)

# =====================================
# PREDICTION BUTTON
# =====================================

predict_button = st.button("🚀 Run AI System Analysis")

if predict_button:

    # NOW USING 7 FEATURES
    input_data = np.array([[
        cpu,
        memory,
        error,
        response,
        threads,
        network,
        disk
    ]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1] * 100
    failure_next_5min = "YES" if prediction[0] == 1 else "NO"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.divider()
    st.subheader("🔮 Predictive Analysis")

    st.write(f"Crash Probability: {probability:.2f}%")
    st.write(f"Timestamp: {timestamp}")

    if prediction[0] == 1:
        st.error("⚠️ High Risk of System Crash!")
    else:
        st.success("✅ System Operating Normally")

    # =====================================
    # DIAGNOSTIC LAYER
    # =====================================

    st.subheader("🔍 Root Cause Analysis")

    root_causes = []

    if cpu > 85:
        root_causes.append("CPU Saturation Detected")
    if memory > 85:
        root_causes.append("High Memory Utilization")
    if error > 7:
        root_causes.append("Error Spike Detected")
    if response > 400:
        root_causes.append("High Response Latency")
    if threads > 800:
        root_causes.append("High Thread Count")
    if network > 800:
        root_causes.append("High Network Traffic")
    if disk > 400:
        root_causes.append("Heavy Disk I/O Activity")

    if len(root_causes) == 0:
        st.info("No critical anomalies detected.")
    else:
        for cause in root_causes:
            st.warning(f"• {cause}")

    # =====================================
    # PRESCRIPTIVE LAYER
    # =====================================

    st.subheader("🛠 Recommended Actions")

    solutions = []

    if cpu > 85:
        solutions.append("Scale CPU resources.")
    if memory > 85:
        solutions.append("Investigate memory leaks.")
    if threads > 800:
        solutions.append("Check for thread leaks or runaway processes.")
    if network > 800:
        solutions.append("Analyze unusual network traffic patterns.")
    if disk > 400:
        solutions.append("Optimize disk-intensive operations.")

    if len(solutions) == 0:
        st.success("System stable. No corrective action required.")
    else:
        for solution in solutions:
            st.write(f"• {solution}")

    # =====================================
    # SAVE LOG
    # =====================================

    new_log = pd.DataFrame({
        "Timestamp": [timestamp],
        "CPU": [cpu],
        "Memory": [memory],
        "Error": [error],
        "Response": [response],
        "Threads": [threads],
        "Network_Traffic": [network],
        "Disk_IO": [disk],
        "Crash_Probability": [probability],
        "Failure_Next_5min": [failure_next_5min]
    })

    history = pd.concat([history, new_log], ignore_index=True)
    history.to_csv(log_file, index=False)

# =====================================
# TREND SECTION
# =====================================

# =====================================
# TREND SECTION
# =====================================

st.subheader("📈 System Trend Graphs")

if len(history) > 1:

    history["Timestamp"] = pd.to_datetime(history["Timestamp"])
    history = history.sort_values("Timestamp")
    history.set_index("Timestamp", inplace=True)

    st.markdown("### 🔥 Core System Trends")

    col1, col2 = st.columns(2)

    # CPU Trend
    with col1:
        st.markdown("#### CPU Usage Trend")
        st.line_chart(history["CPU"])

    # Memory Trend
    with col2:
        st.markdown("#### Memory Usage Trend")
        st.line_chart(history["Memory"])

    st.markdown("---")
    st.markdown("### 🌐 Advanced Resource Trends")

    col3, col4 = st.columns(2)

    # Network Trend
    with col3:
        st.markdown("#### Network Traffic Trend")
        st.line_chart(history["Network_Traffic"])

    # Disk Trend
    with col4:
        st.markdown("#### Disk I/O Trend")
        st.line_chart(history["Disk_IO"])

    st.markdown("---")

    # Thread Trend Full Width
    st.markdown("#### Thread Activity Trend")
    st.line_chart(history["Threads"])

else:
    st.info("Not enough data to show trends yet. Run analysis multiple times.")

# =====================================
# HISTORY TABLE
# =====================================

st.subheader("📜 System History")

if len(history) > 0:
    st.dataframe(history.tail(10))
else:
    st.info("No historical data yet.")