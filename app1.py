import streamlit as st
import psutil
import plotly.graph_objects as go
import time

# st.set_page_config(layout="wide", page_title="AI-Powered Performance Analyzer")

st.title("System Performance Monitor")


def system_performance():
    st.title("📊 System Performance Monitoring")
    st.write("This page monitors system performance in real time.")
    
if __name__ == "__main__":
    system_performance()


# Function to get system stats
def get_stats():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    
    return {
        "cpu": cpu_usage,
        "memory": memory.percent,
        "disk": disk.percent,
        "network": (net.bytes_sent / (1024 * 1024), net.bytes_recv / (1024 * 1024))
    }

# Layout for monitoring
col1, col2 = st.columns(2)

with col1:
    st.subheader("CPU Usage")
    cpu_chart = st.empty()
    
with col2:
    st.subheader("Memory Usage")
    mem_chart = st.empty()

st.subheader("Disk Usage")
disk_chart = st.empty()

st.subheader("Network Activity (MB Sent/Received)")
net_chart = st.empty()

# Fetch data and update UI
stats = get_stats()

# CPU Chart
cpu_fig = go.Figure(go.Bar(x=[f"Core {i}" for i in range(len(stats["cpu"]))], y=stats["cpu"]))
cpu_fig.update_layout(yaxis=dict(range=[0, 100]), title="CPU Usage per Core")
cpu_chart.plotly_chart(cpu_fig, use_container_width=True)

# Memory Chart
mem_fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=stats["memory"],
    title="Memory Usage",
    gauge={"axis": {"range": [0, 100]}}
))
mem_chart.plotly_chart(mem_fig, use_container_width=True)

# Disk Chart
disk_fig = go.Figure(go.Indicator(
    mode="gauge+number",
    value=stats["disk"],
    title="Disk Usage",
    gauge={"axis": {"range": [0, 100]}}
))
disk_chart.plotly_chart(disk_fig, use_container_width=True)

# Network Chart
net_fig = go.Figure(data=[
    go.Bar(name="Bytes Sent", x=["Network"], y=[stats["network"][0]]),
    go.Bar(name="Bytes Received", x=["Network"], y=[stats["network"][1]])
])
net_fig.update_layout(barmode='group', title="Network Data Transfer (MB)")
net_chart.plotly_chart(net_fig, use_container_width=True)

# Auto-refresh every 2 seconds
refresh_rate = st.slider("Refresh Interval (seconds)", 2, 10, 5)  # Min 2s, Max 10s, Default 5s
time.sleep(refresh_rate)
st.rerun()


