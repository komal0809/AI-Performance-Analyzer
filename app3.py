import streamlit as st
import psutil
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go

# st.set_page_config(layout="wide", page_title="AI-Powered Performance Analyzer")

st.title("🔍 AI-Powered System Performance Analyzer")

# **PROCESS MONITORING**
st.subheader("📊 Live Process Monitoring")

import streamlit as st
def ai_system_performance_analyzer():
    st.title("🤖 AI-Powered System Performance Analyzer")
    st.write("This page analyzes system performance using AI.")

if __name__ == "__main__":
    ai_system_performance_analyzer()


def get_process_list():
    process_list = []
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_list.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue  # Ignore processes that no longer exist
    return pd.DataFrame(process_list)

# Sorting dropdown
sort_option = st.selectbox("Sort by:", ["CPU Usage", "Memory Usage"], index=0)
process_df = get_process_list()

# Sort the data
if sort_option == "CPU Usage":
    process_df = process_df.sort_values(by="cpu_percent", ascending=False)
else:
    process_df = process_df.sort_values(by="memory_percent", ascending=False)

# Display process table
st.dataframe(process_df, height=400)

# **KILL A PROCESS**
st.subheader("🛑 Kill a Process")
pid_to_kill = st.text_input("Enter PID to Kill:")
if st.button("Terminate Process"):
    try:
        psutil.Process(int(pid_to_kill)).terminate()
        st.success(f"✅ Process {pid_to_kill} terminated successfully!")
    except psutil.NoSuchProcess:
        st.error(f"❌ Process {pid_to_kill} no longer exists.")
    except psutil.AccessDenied:
        st.error(f"❌ Permission denied. Run as administrator.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# **PROCESS SCHEDULING ANALYSIS**
st.subheader("⏳ Process Scheduling Efficiency")

# Track CPU Burst Times (Simulated)
cpu_burst_times = {}
for proc in psutil.process_iter():
    try:
        cpu_burst_times[proc.pid] = proc.cpu_percent()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue  # Skip if the process no longer exists

# Convert to DataFrame
burst_df = pd.DataFrame(cpu_burst_times.items(), columns=["PID", "CPU Burst Time"])
burst_df = burst_df.sort_values(by="CPU Burst Time", ascending=False)

# **CPU Burst Time Bar Chart**
fig_burst = px.bar(burst_df, x="PID", y="CPU Burst Time", title="CPU Burst Time per Process", color="CPU Burst Time")
st.plotly_chart(fig_burst, use_container_width=True)

# **CONTEXT SWITCH ANALYSIS**
context_switches = psutil.cpu_stats().ctx_switches
st.metric("🔄 Context Switches", context_switches)

# **LIVE CPU USAGE CHART**
cpu_usage = []
pids = []

for proc in psutil.process_iter():
    try:
        cpu_usage.append(proc.cpu_percent())
        pids.append(proc.pid)
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        continue  # Skip if the process no longer exists

fig_cpu = go.Figure()
fig_cpu.add_trace(go.Bar(x=pids, y=cpu_usage, name="CPU Usage"))

fig_cpu.update_layout(
    title="Live CPU Usage Per Process",
    xaxis_title="Process ID",
    yaxis_title="CPU Usage (%)",
)

st.plotly_chart(fig_cpu, use_container_width=True)

# **Auto-refresh every 5 seconds**
time.sleep(5)
st.rerun()
