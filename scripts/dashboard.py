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
        [data-testid="stMain"] {
            overflow: hidden !important; /* Prevent scrolling */
        }
        /* Light theme enforcement */
        [data-testid="stAppViewContainer"] {
            background-color: #f7f7f7;
            top: -7rem;
            overflow: hidden !important;
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
            overflow: hidden !important;
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
            # padding-bottom: 1rem;
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
            color: rgb(242, 102, 43);
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
            overflow: hidden !important;
        }
            
        [data-testid="stDataFrameResizable"] {
            resize: none !important;
            pointer-events: none !important;
        }

        /* Navigation text color */
        [data-testid="stSidebarNav"] {
            color: white;
        }
        [data-testid="stSidebarNav"] .nav-link {
            color: white !important;
        }
            
        [data-testid="stDataFrame"] {
            resize: none !important; /* Disable resizing */
            overflow: hidden !important;
        }
            
        [data-testid="stElementToolbar"] {
            display: none !important;
        }
            
        /* Hide default toolbar */
        [data-testid="stToolbar"] {
            display: none;
        }
            
        [data-testid="stRadio"] input[type="radio"] {
            display: none !important;
        }
            
        [data-testid="stWidgetLabel"] {
            display: none !important;
        }
  
        [data-testid="stRadio"] label {
            display: flex;
            background-color: #ffffff;
            color: #323393;
            border: 2px solid #323393;
            border-radius: 10px; /* Rounded corners */
            padding: 0.5rem 1rem;
            margin: 0.2rem;
            cursor: pointer;
            font-weight: bold;
            text-align: center;
            transition: background-color 0.3s, color 0.3s, transform 0.1s;
            width:100%;
        }
        
        /* Dashboard Button */
        [data-testid="stRadio"] label:nth-of-type(1)::before {
            content: "📊";
            font-size: 1.2rem;
            margin-right: 0.5rem; /* Space between icon and text */
        }

        /* Map Button */
        [data-testid="stRadio"] label:nth-of-type(2)::before {
            content: "🎢";
            font-size: 1.2rem;
            margin-right: 0.5rem;
        }
            
        [data-testid="stHeaderActionElements"] {
            display: none;
        }
            
    </style>
""", unsafe_allow_html=True)

st.header("Port Aventura World - Attraction Wait Times")
# Sidebar
with st.sidebar:
    st.header("Navigation")
    selected_page = st.radio("Choose a view", ["Dashboard", "Park Map"], label_visibility="collapsed")

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
        ["10:30"],
        index=0
    )

with top_col4:
    st.metric(
        "Current Attendance",
        "5,000",
        "500 from yesterday",
        delta_color="normal"
    )

# Main content
if selected_page == "Dashboard":
    # Two columns layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current Attraction Status")

        # Model predictions to be added here
        attractions_data = {
            'ENTITY_DESCRIPTION_SHORT': ['Dizzy Dropper', 'Sling Shot', 'Gondola', 'Monorail', 'Top Spin', 'Skyway', 'Sling Shot', 'Gondola', 'Free Fall', 'Inverted Coaster'],
            'CAPACITY': [1000, 800, 600, 555, 750, 1200, 900, 700, 500, 1000],
            'OPEN_TIME': ['10:00', '10:00', '10:00', '10:00', '10:30', '10:30', '10:30', '10:30', '10:30', '10:30'],
            'DOWNTIME': [0, 15, 0, 0, 10, 0, 0, 15, 5, 0],
            'WAIT_TIME': [45, 30, 20, 50, 10, 20, 0, 5, 22, 10]
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

        styled_df = df.style.map(highlight_long_waits, subset=['WAIT_TIME'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Park Metrics")
        avg_wait = df['WAIT_TIME'].mean()
        max_wait = df['WAIT_TIME'].max()
        rides_down = df[df['DOWNTIME'] > 0].shape[0]
        
        st.metric("Average Wait Time", f"{int(avg_wait)} min")
        st.metric("Maximum Wait Time", f"{int(max_wait)} min")
        st.metric("Rides Currently Down", rides_down)

else:  # Map view
    # Add the title for the map view
    st.markdown("<h1 style='text-align: center; color: #323393;top:-5rem;position:relative;'>Amusement Park Map</h1>", unsafe_allow_html=True)

    # Placeholder data for attractions
    attractions = [
        {"name": 'Dizzy Dropper', "metric": "45 min wait", "status": "open"},
        {"name": 'Sling Shot', "metric": "15 min wait", "status": "closed"},
        {"name": 'Gondola', "metric": "30 min wait", "status": "open"},
        {"name": 'Monorail', "metric": "10 min wait", "status": "open"},
        {"name": 'Top Spin', "metric": "50 min wait", "status": "closed"},
        {"name": 'Skyway', "metric": "5 min wait", "status": "open"},
        {"name": 'Sling Shot', "metric": "25 min wait", "status": "open"},
        {"name": 'Gondola', "metric": "20 min wait", "status": "closed"},
        {"name": 'Free Fall', "metric": "35 min wait", "status": "open"},
        {"name": 'Inverted Coaster', "metric": "40 min wait", "status": "open"},
    ]

    # Create a grid layout
    grid_cols = st.columns(2)  # Two columns to arrange the SVGs

    for i, attraction in enumerate(attractions):
        with grid_cols[i % 2]:  # Alternate between two columns
            color = "#ffffff" if attraction["status"] == "open" else "#cccccc"  # Gray if closed
            filter_style = "grayscale(1); opacity: 0.5;" if attraction["status"] == "closed" else "none;"
            st.markdown(f"""
                <div style="top:-5rem;position:relative;display: flex; align-items: center; margin: 1rem; background-color: {color}; padding: 1rem; border-radius: 10px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
                    <div style="flex-shrink: 0; width: 80px; height: 80px; margin-right: 1rem;">
                       <?xml version="1.0" encoding="iso-8859-1"?>
<!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
<svg height="5rem" width="5rem" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
	 viewBox="0 0 512 512" xml:space="preserve">
<path style="fill:#E61F00;" d="M270.747,263.511v56.763H165.18l-48.027-88.483L73.12,251.247
	c-16.872,7.455-27.755,24.163-27.755,42.607v121.579h425.719v-61.8c0-25.404-17.501-47.46-42.241-53.232L270.747,263.511z"/>
<path style="fill:#58555D;" d="M136.637,284.379c-9.22,0-16.696-7.475-16.696-16.696V72.913c0-9.22,7.475-16.696,16.696-16.696
	c9.22,0,16.696,7.475,16.696,16.696v194.77C153.333,276.904,145.858,284.379,136.637,284.379z"/>
<path style="fill:#3C3A3F;" d="M136.637,56.218v228.162c9.22,0,16.696-7.475,16.696-16.696V72.913
	C153.333,63.693,145.858,56.218,136.637,56.218z"/>
<path style="fill:#A51000;" d="M428.845,300.402l-158.097-36.891v56.763h-14.716v95.161h215.052v-61.8
	C471.085,328.23,453.583,306.174,428.845,300.402z"/>
<path style="fill:#3C3A3F;" d="M270.747,336.968H165.181c-6.122,0-11.754-3.351-14.673-8.732l-48.026-88.483
	c-4.399-8.103-1.395-18.239,6.708-22.638c8.106-4.397,18.239-1.395,22.638,6.709l43.287,79.751h78.936v-20.543l-14.501-21.758
	c-5.113-7.673-3.039-18.039,4.634-23.152c7.672-5.113,18.038-3.039,23.152,4.632l17.303,25.963c1.829,2.743,2.804,5.964,2.804,9.259
	v42.293C287.442,329.494,279.967,336.968,270.747,336.968z"/>
<path style="fill:#797882;" d="M473.602,455.782H38.398C17.191,455.782,0,438.591,0,417.385l0,0
	c0-21.207,17.191-38.398,38.398-38.398h435.204c21.207,0,38.398,17.191,38.398,38.398l0,0
	C512,438.591,494.809,455.782,473.602,455.782z"/>
<path style="fill:#8B8990;" d="M233.177,289.946c-3.548,0-7.125-1.128-10.157-3.455c-7.313-5.616-8.69-16.097-3.073-23.411
	l34.556-45.003c5.615-7.314,16.098-8.687,23.411-3.074c7.313,5.616,8.69,16.097,3.074,23.411l-34.557,45.003
	C243.143,287.699,238.188,289.946,233.177,289.946z"/>
<path style="fill:#3E3E42;" d="M473.602,378.986H256v76.797h217.602c21.207,0,38.398-17.191,38.398-38.398l0,0
	C512,396.178,494.809,378.986,473.602,378.986z"/>
</svg>
                    </div>
                    <div>
                        <h3 style="margin: 0; color: #323393;">{attraction["name"]}</h3>
                        <p style="margin: 0; color: #323393;">{attraction["metric"]}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)