import streamlit as st

# ✅ Set Page Config (Only Once!)
st.set_page_config(page_title="System Analyzer", page_icon="🖥", layout="wide")

# 🛠 Sidebar Navigation
st.sidebar.title("🔍 Navigation")
selected_page = st.sidebar.radio("Select a Page:", ["Home", "System Monitor", "Gantt Chart"])

# ✅ Only One System Monitor (Merged AI Analyzer + System Performance)
if selected_page == "Home":
    st.title("🏠 Home - System Analyzer")
    st.write("Welcome to the **System Analyzer Dashboard**! Use the sidebar to navigate.")

elif selected_page == "System Monitor":
    from app1 import system_performance
    system_performance()

elif selected_page == "Gantt Chart":
    from app4 import process_gantt_chart
    process_gantt_chart()
