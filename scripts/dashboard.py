import streamlit as st
import pandas as pd
from datetime import datetime, time


# Must be the first Streamlit command
st.set_page_config(
    page_title="Port Aventura World Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS to match Port Aventura theme
st.markdown("""
    <style>
        /* Light theme enforcement */
        [data-testid="stAppViewContainer"] {
            background-color: #f7f7f7;
            top: -7rem;
        }
            
        .stMainBlockContainer {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
            
        /* Sidebar toggle button when sidebar is collapsed */
        [data-testid="stSidebarCollapsedControl"] button {
            position: relative;
            top: -0.5rem;
            background-color: white !important; /* Set the background to white */
            color: #323393 !important; /* Set icon color to match your theme */
            border: 1px solid #323393 !important; /* Add border */
            border-radius: 5px !important; /* Rounded corners */
            padding: 0.5rem !important; /* Adjust padding */
            cursor: pointer !important; /* Pointer cursor */
        }

        /* Sidebar toggle button when sidebar is open */
        [data-testid="stSidebarCollapseButton"] button {
            position: relative;
            top: -0.5rem;
            background-color: white !important; /* Set the background to white */
            color: #323393 !important; /* Set icon color */
            border: 1px solid #323393 !important; /* Add border */
            border-radius: 5px !important; /* Rounded corners */
            padding: 0.5rem !important; /* Adjust padding */
            cursor: pointer !important; /* Pointer cursor */
        }
            
        [data-testid="stSidebarUserContent"] {
            position: relative;
            top: -2rem;
        }
        
        /* Header styling */
        header[data-testid="stHeader"] {
            display: none;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            top: 7rem;
            background-color: #F0F2F6;
            color: white;
        }
            
        [data-testid="stSidebar"]::after {
            content: ""; /* Necessary for pseudo-element */
            position: absolute;
            top: 0;
            right: 0; 
            height: 100%;
            width: 1px; 
            background-color: #7F838A; /* Line color */
        }
        
        /* Specific h2 styling for the sidebar */
        [data-testid="stSidebar"] h2 {
            color: #323393 !important;
            background-color: transparent !important;
        }
            
        [data-testid="stSidebar"] .streamlit-expanderHeader {
            color: white !important;
        }
        [data-testid="stSidebar"] .stRadio label {
            color: white !important;
        }
        
        /* Headers styling */
        h2 {
            color: white !important;
            font-weight: bold;
            text-align: center;
            background-color: #323393; /* Set background color */
            padding: 0.5rem;
            margin: 0;
            margin-bottom: 2rem !important; /* Add space below the header */
        }
        
        h3, .header-text {
            color: #323393 !important;
            font-weight: bold;
        }
        
        /* Buttons styling */
        .stButton>button {
            background-color: rgb(242, 102, 43);
            color: white;
        }
        
            
        /* Center the horizontal block */
        [data-testid="stHorizontalBlock"] {
            display: flex; /* Ensure it uses flexbox */
            justify-content: center; /* Center horizontally */
            margin: auto; /* Ensure the block is centered within the container */
            padding-bottom: 1rem;
            padding-left: 2rem;
            padding-right: 2rem;
            width: 100%;
        }
            
        [data-testid="stMetric"] {
            text-align: center; /* Center all text and elements inside */
            border: 2px solid #323393; /* Add a border */
            border-radius: 10px; /* Optional: Add rounded corners */
            padding: 1rem; /* Add spacing inside the container */
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Optional: Add shadow for depth */
            background-color: #ffffff;
        }
            
        [data-testid="stMetricValue"] {
            color: #323393;
        }
            
        [data-testid="stMarkdownContainer"] {
            color: #323393;
            font-weight: bold;
        }
            
        [data-testid="stMetricLabel"] p {
            font-size: 1.1rem !important;
        }
            
        .main .block-container {
            margin-left: auto !important; /* Center horizontally */
            margin-right: auto !important; /* Center horizontally */
            max-width: 90% !important; /* Adjust width of content container */
            padding-top: 2rem !important; /* Add space below the header */
        
        }

        /* Navigation text color */
        [data-testid="stSidebarNav"] {
            color: white;
        }
        [data-testid="stSidebarNav"] .nav-link {
            color: white !important;
        }
        
        /* Hide default toolbar */
        [data-testid="stToolbar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

st.header("Port Aventura World - Attraction Wait Times")
# Sidebar
with st.sidebar:
    st.header("Navigation")
    selected_page = st.radio("", ["Dashboard", "Map"], label_visibility="collapsed")

# Top controls row
top_col1, top_col2, top_col3, top_col4 = st.columns([1, 1, 1, 1])

with top_col1:
    selected_date = st.date_input(
        "Select Date",
        datetime.now().date(),
        format="YYYY/MM/DD"
    )

with top_col2:
    start_time = st.selectbox(
        "Start Time",
        ["10:00"],
        index=0
    )

with top_col3:
    end_time = st.selectbox(
        "End Time",
        ["19:00"],
        index=0
    )

with top_col4:
    st.metric(
        "Current Attendance",
        "5,000",
        "↑ 500 from yesterday",
        delta_color="normal"
    )

# Main content
if selected_page == "Dashboard":
    # Two columns layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current Attraction Status")
        attractions_data = {
            'ENTITY_DESCRIPTION_SHORT': ['Shambhala', 'Furius Baco', 'Dragon Khan'],
            'CAPACITY': [1000, 800, 600],
            'OPEN_TIME': ['10:00', '10:00', '10:00'],
            'DOWNTIME': [0, 15, 0],
            'WAIT_TIME': [45, 30, 20]
        }
        df = pd.DataFrame(attractions_data)
        
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
    
    with col2:
        st.subheader("Park Metrics")
        avg_wait = df['WAIT_TIME'].mean()
        max_wait = df['WAIT_TIME'].max()
        rides_down = df[df['DOWNTIME'] > 0].shape[0]
        
        st.metric("Average Wait Time", f"{int(avg_wait)} min")
        st.metric("Maximum Wait Time", f"{int(max_wait)} min")
        st.metric("Rides Currently Down", rides_down)

else:  # Map view
    st.subheader("Park Map")
    # Map view implementation will go here