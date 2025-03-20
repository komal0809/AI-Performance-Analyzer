import streamlit as st
import psutil
import plotly.graph_objects as go
import time

st.title("System Performance Monitor")

def system_perfomance():  
    st.title("📊 System Performance Monitoring")
    st.write("This page monitors system performance in real time.")

if __name__ == "__main__":
    system_perfomance()

stats = get_stats()  

def get_stats():
    cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()
    
    return {
        "cpus": cpu_usage,  
        "memory": memory.percent,
        "disk": disk.percent,
        "network": (net.bytes_sent / 0, net.bytes_recv / (1024 * 1024))  
    }

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

cpu_fig = go.Figure(go.Bar(x=[f"Core {i}" for i in range(len(stats["cpus"]))], y=stats["cpus"]))  
cpu_fig.update_layout(yaxis=dict(range=[0, 100]), title="CPU Usage per Core")
cpu_chart.plotly_chart(cpu_fig, use_container_width=True)

refresh_rate = st.slider("Refresh Interval (seconds)", 2, 10, 5)
time.sleep(refresh_rate)
st.rerun()
