import streamlit as st
import psutil
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

def process_gantt_chart():
    st.title("📊 Real-Time Process Gantt Chart")
    st.write("This page displays a real-time Gantt chart of system processes.")

    def get_top_processes(n=5):
        processes = []
        # Call once to initialize CPU percent measurement
        psutil.cpu_percent(interval=None)
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                cpu = proc.info['cpu_percent']
                if cpu is not None and cpu > 0:  # Check for None and ignore idle processes
                    processes.append((proc.info['pid'], proc.info['name'], cpu))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        processes.sort(key=lambda x: x[2], reverse=True)  # Sort by CPU usage
        return processes[:n]

    def create_process_table():
        processes = get_top_processes()
        start_times = np.linspace(0, 10, len(processes))  # Simulated arrival times
        burst_times = np.random.randint(3, 10, len(processes))  # Simulated burst times
        end_times = start_times + burst_times

        df = pd.DataFrame({
            'Process': [p[1] for p in processes],
            'Start Time': start_times,
            'Burst Time': burst_times,
            'End Time': end_times
        })
        return df

    def plot_gantt_chart(df):
        fig, ax = plt.subplots(figsize=(8, 4))
        for i, row in df.iterrows():
            ax.barh(row['Process'], row['Burst Time'], left=row['Start Time'], color=np.random.rand(3,))

        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_title('Process Scheduling Gantt Chart')
        return fig

    # Display process table
    df = create_process_table()
    st.write('### Process Table')
    st.dataframe(df)

    # Display Gantt Chart
    st.write('### Gantt Chart')
    fig = plot_gantt_chart(df)
    st.pyplot(fig)

    # Auto-refresh every 5 seconds
    time.sleep(5)
    st.rerun()

# Run the function
if __name__ == "__main__":
    process_gantt_chart()
