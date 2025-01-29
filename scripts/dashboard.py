import streamlit as st
import pandas as pd
from datetime import datetime, time
import plotly.express as px

# Set page config
st.set_page_config(page_title="Nom Park Dashboard", layout="wide")

# Title and description
st.title("Nom Park - Attraction Wait Times")
st.markdown("### Real-time Attraction Monitoring Dashboard")

# Create sidebar for inputs
with st.sidebar:
    st.header("Dashboard Controls")
    
    # Date selector
    selected_date = st.date_input(
        "Select Date",
        datetime.now().date()
    )
    
    # Attendance input
    attendance = st.number_input(
        "Park Attendance",
        min_value=0,
        max_value=100000,
        value=5000
    )
    
    # Time range selector
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.time_input(
            "Start Time",
            time(9, 0)  # Default 9:00 AM
        )
    with col2:
        end_time = st.time_input(
            "End Time",
            time(22, 0)  # Default 10:00 PM
        )

# Main content
# Sample data - Replace this with your actual data and model predictions
attractions_data = {
    'ENTITY_DESCRIPTION_SHORT': ['Roller Coaster X', 'Water Ride Y', 'Family Ride Z'],
    'CAPACITY': [1000, 800, 600],
    'OPEN_TIME': ['09:00', '10:00', '09:00'],
    'DOWNTIME': [30, 0, 15],
    'REF_CLOSING_DESCRIPTION': ['Technical Issue', 'None', 'Maintenance'],
    'WAIT_TIME': [45, 30, 20]  # Replace with your model predictions
}
df = pd.DataFrame(attractions_data)

# Create two columns for the main content
col1, col2 = st.columns([2, 1])

with col1:
    # Main attractions table
    st.subheader("Current Attraction Status")
    
    # Style the dataframe
    def highlight_long_waits(val):
        if isinstance(val, (int, float)):
            if val >= 45:
                return 'background-color: #ffcccc'
            elif val >= 30:
                return 'background-color: #fff2cc'
            return ''
        return ''
    
    styled_df = df.style.applymap(highlight_long_waits, subset=['WAIT_TIME'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Wait times chart
    st.subheader("Wait Times Overview")
    fig = px.bar(df, 
                 x='ENTITY_DESCRIPTION_SHORT', 
                 y='WAIT_TIME',
                 title='Current Wait Times by Attraction',
                 color='WAIT_TIME',
                 color_continuous_scale=['green', 'yellow', 'red'])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Summary metrics
    st.subheader("Park Metrics")
    
    # Calculate metrics
    avg_wait = df['WAIT_TIME'].mean()
    max_wait = df['WAIT_TIME'].max()
    rides_down = df[df['DOWNTIME'] > 0].shape[0]
    
    # Display metrics in boxes
    st.metric("Average Wait Time", f"{avg_wait:.0f} min")
    st.metric("Maximum Wait Time", f"{max_wait:.0f} min")
    st.metric("Rides Currently Down", rides_down)
    
    # Capacity utilization chart
    st.subheader("Capacity Utilization")
    fig2 = px.pie(df, 
                  values='CAPACITY', 
                  names='ENTITY_DESCRIPTION_SHORT',
                  title='Attraction Capacity Distribution')
    st.plotly_chart(fig2, use_container_width=True)

# Footer with timestamp
st.markdown("---")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")