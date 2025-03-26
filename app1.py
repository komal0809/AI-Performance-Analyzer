import streamlit as st
import psutil
import plotly.graph_objects as go
import time

def system_performance():
    st.title("📊 System Monitor - AI Enhanced Performance Analysis")

    # 🛠 Sidebar Controls
    with st.sidebar:
        st.subheader("⚙️ Settings")
        refresh_rate = st.slider("Refresh Interval (seconds)", 1, 10, 5)
        dark_mode = st.toggle("🌙 Dark Mode")
        selected_metrics = st.multiselect(
            "📊 Select Metrics to Display:",
            ["CPU Usage", "Memory Usage", "Disk Usage", "Network Activity"],
            default=["CPU Usage", "Memory Usage", "Disk Usage", "Network Activity"]
        )

    theme = "plotly_dark" if dark_mode else "plotly"

    # 🎯 Function to Get System Stats
    def get_stats():
        return {
            "cpu": psutil.cpu_percent(interval=1, percpu=True),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "network": (
                psutil.net_io_counters().bytes_sent / (1024 * 1024),
                psutil.net_io_counters().bytes_recv / (1024 * 1024)
            )
        }

    stats = get_stats()

    # 🚨 Alert for High Usage
    if stats["cpu"][0] > 80:
        st.warning("⚠️ High CPU Usage Detected!")
    if stats["memory"] > 85:
        st.error("🚨 Critical Memory Usage! Consider closing some applications.")

    # 🔄 Tabs for Interactivity
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 CPU Usage", "💾 Memory", "📀 Disk", "🌐 Network"])

    if "CPU Usage" in selected_metrics:
        with tab1:
            st.subheader("🔥 CPU Usage")
            cpu_fig = go.Figure(go.Bar(x=[f"Core {i}" for i in range(len(stats["cpu"]))], y=stats["cpu"]))
            cpu_fig.update_layout(yaxis=dict(range=[0, 100]), title="CPU Usage per Core", template=theme)
            st.plotly_chart(cpu_fig, use_container_width=True)

    if "Memory Usage" in selected_metrics:
        with tab2:
            st.subheader("💾 Memory Usage")
            mem_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stats["memory"],
                title="Memory Usage",
                gauge={"axis": {"range": [0, 100]}}
            ))
            mem_fig.update_layout(template=theme)
            st.plotly_chart(mem_fig, use_container_width=True)

    if "Disk Usage" in selected_metrics:
        with tab3:
            st.subheader("📀 Disk Usage")
            disk_fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=stats["disk"],
                title="Disk Usage",
                gauge={"axis": {"range": [0, 100]}}
            ))
            disk_fig.update_layout(template=theme)
            st.plotly_chart(disk_fig, use_container_width=True)

    if "Network Activity" in selected_metrics:
        with tab4:
            st.subheader("🌐 Network Activity")
            net_fig = go.Figure(data=[
                go.Bar(name="Bytes Sent", x=["Network"], y=[stats["network"][0]]),
                go.Bar(name="Bytes Received", x=["Network"], y=[stats["network"][1]])
            ])
            net_fig.update_layout(barmode='group', title="Network Data Transfer (MB)", template=theme)
            st.plotly_chart(net_fig, use_container_width=True)

    # 🔄 Auto-Refresh Every X Seconds
    time.sleep(refresh_rate)
    st.rerun()
