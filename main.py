import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
from matplotlib.colors import LinearSegmentedColormap
from streamlit_webrtc import webrtc_streamer  # Ensure this is imported for webcam streaming

# Load the dataset (adjust the path if needed)
try:
    # Load dataset from CSV file
    df = pd.read_csv('medications.csv')  # Path to your CSV file
except Exception as e:
    st.error(f"Error loading the dataset: {e}")
    df = None

# Set Up Login Variables
premium_credentials = {
    "prime": "primepass",
}
premium_plus_credentials = {
    "elite": "elitepass",
}

# Video frame callback to process the webcam feed and detect medication
def video_frame_callback(frame):
    # Convert frame to RGB
    img = frame.to_image()
    img = np.array(img)
    
    # Apply medication detection on the image
    if df is not None:
        detected_name = df['Drug Name'].iloc[0]  # Return the first medication for now

        # Display the detected medication name below the image
        if detected_name:
            st.write(f"### Detected Medication: {detected_name}")

    # Convert image back to format streamlit_webrtc expects
    return frame

# Function for checking credentials
def check_credentials(username, password):
    if premium_credentials.get(username) == password:
        return "authenticated"
    elif premium_plus_credentials.get(username) == password:
        return "authenticated_plus"
    return None

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "authenticated_plus" not in st.session_state:
    st.session_state.authenticated_plus = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Placeholder for login status
login_placeholder = st.empty()

# Page content rendering
def render_page(selected):
    if selected == "Scanning":
        st.title("Scanning Page")
        selected = option_menu(
            menu_title=None,
            options=["Scan", "Search"],
            icons=["camera", "search"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
        if selected == "Scan":
            # scanning_page() # Calling Scanning Page
            # Scanning Page Code
            st.write("Use your camera to scan medication.")
            
            # Display the detected medication below the webcam feed
            if df is not None:
                # Use webcam stream with streamlit_webrtc
                webrtc_ctx = webrtc_streamer(
                    key="example", 
                    video_frame_callback=video_frame_callback,
                    media_stream_constraints={"video": True, "audio": False},
                    video_html_attrs={"width": "100%"}
                )

                # Display the detected medication info below
                if webrtc_ctx and webrtc_ctx.state.playing:
                    # Process a dummy frame for detection
                    detected_name = video_frame_callback(None)  # Simulate detection logic
                    if detected_name:
                        medication_info = df[df['Drug Name'] == detected_name].iloc[0]
                        st.write(f"### Medication Info:")
                        st.write(f"**Drug Name**: {medication_info['Drug Name']}")
                        st.write(f"**Drug Class**: {medication_info['Drug Class']}")
                        st.write(f"**Description**: {medication_info['Description']}")
                        st.write(f"**Side Effects**: {medication_info['Side Effects']}")
                        st.write(f"**Active Ingredients**: {medication_info['Active Ingredients']}")

            
        elif selected == "Search":
            # scanning_page() # Calling Search Page
            st.title("Search Page")
            def search_medication(med_name):
    if df is not None and 'name' in df.columns:
        return df[df['name'].str.contains(med_name, case=False, na=False)]
    return pd.DataFrame()

# Function for selecting a specific medication
def display_medication_options(search_results):
    if not search_results.empty:
        selected_med = st.selectbox("Select the specific medication:", search_results['name'].unique(), key="med_select")
        if selected_med:
            specific_med = search_results[search_results['name'] == selected_med].iloc[0]
            side_effects = [specific_med[col] for col in df.columns if 'sideEffect' in col and not pd.isna(specific_med[col])][:3]
            st.write(f"### Medication Name: {specific_med['name']}")
            st.write(f"**Side Effects:** {', '.join(side_effects)}")
    else:
        st.write("No medication found.")

# Page content rendering
def render_page(selected):
    if selected == "Scanning":
        st.title("Scanning Page")
        selected = option_menu(None, ["Scan", "Search"], icons=["camera", "search"], menu_icon="cast", default_index=0, orientation="horizontal")
        if selected == "Search":
            st.title("Search Medication")
            search_query = st.text_input("Enter Medication Name:", key="search_query").strip()
            if search_query:
                search_results = search_medication(search_query)
                display_medication_options(search_results)

    elif selected == "Management":
        st.title("Management Page")
        st.write("This is the management page.")

    elif selected == "History":
        st.title("History Page")
        st.write("This is the history page.")

    elif selected == "Delivery":
        st.title("Delivery Page")
        st.write("This is the delivery page.")

    elif selected == "Premium":
        # render_premium_page()  # Calling Premium Page File
        # Render the premium page content
        st.markdown("""
            <style>
                .premium-title {
                    font-size: 36px;
                    font-weight: bold;
                    color: #2C3E50;
                    text-align: center;
                }
                .premium-subtitle {
                    font-size: 24px;
                    font-weight: bold;
                    color: #2980B9;
                }
                .premium-card {
                    border: 2px solid #2980B9;
                    border-radius: 10px;
                    padding: 20px;
                    margin-bottom: 20px;
                    background-color: #ECF0F1;
                    text-align: center;
                }
                .premium-button {
                    background-color: #2980B9;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-size: 18px;
                    cursor: pointer;
                }
                .premium-button:hover {
                    background-color: #3498DB;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="premium-title">Choose Your Premium Plan</div>', unsafe_allow_html=True)
        st.markdown("### Enhance your experience with exclusive features and benefits!")

        # Prime Version
        st.write("-"*75)
        col1, col2 = st.columns(2)
        col1.metric(label="Type of Premium", value="Prime")
        col2.metric(label="Price", value="$10")
        st.write("### Features of Prime:")
        prime_features = [
            "✔️ Access to basic AI tools",
            "✔️ Limited cloud storage",
            "✔️ Standard customer support",
            "✔️ Monthly updates"
        ]
        st.write("\n".join(prime_features))
        st.markdown('<button class="premium-button">Purchase Prime</button>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Elite Version
        st.write("-"*75)
        col1, col2 = st.columns(2)
        col1.metric(label="Type of Premium", value="Elite")
        col2.metric(label="Price", value="$20")
        st.write("### Features of Elite:")
        elite_features = [
            "🌟 Full access to all AI tools",
            "🌟 Unlimited cloud storage",
            "🌟 Priority customer support",
            "🌟 Weekly exclusive updates",
            "🌟 Advanced analytics dashboard"
        ]
        st.write("\n".join(elite_features))
        st.markdown('<button class="premium-button">Purchase Elite</button>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Reminder for Premium Plus
        st.markdown("""
            <div style="font-size: 18px; text-align: center; color: #7F8C8D; margin-top: 40px;">
                Upgrade to Premium Plus for the ultimate experience and exclusive benefits!
            </div>
        """, unsafe_allow_html=True)

    elif selected == "Family Plan":
        st.title("Premium Plus Page")
        # Separate Sections
        st.subheader("-" * 75)

# Sidebar Menu
with st.sidebar:
    if st.session_state.authenticated_plus:
        selected = option_menu(
            menu_title="Elite Version",
            options=["Scanning", "Management", "History", "Delivery", "Family Plan", "Log Out"],
            icons=["camera", "calculator-fill", "archive", "truck", "stars", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical"
        )
    elif st.session_state.authenticated:
        selected = option_menu(
            menu_title="Prime Version",
            options=["Scanning", "Management", "History", "Delivery", "Log Out"],
            icons=["camera", "calculator-fill", "archive", "truck", "box-arrow-right"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical"
        )
    else:
        selected = option_menu(
            menu_title="Free",
            options=["Scanning", "Management", "Premium"],
            icons=["camera", "calculator-fill", "cart3"],
            menu_icon="cast",
            default_index=0,
            orientation="vertical"
        )
                
        # Login Form
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            auth_status = check_credentials(username, password)
            if auth_status == "authenticated":
                st.session_state.authenticated = True
                st.success("Prime Login Successful!")
                login_placeholder.empty()  # Remove the login form immediately
            elif auth_status == "authenticated_plus":
                st.session_state.authenticated_plus = True
                st.success("Elite Login Successful!")
                login_placeholder.empty()  # Remove the login form immediately
            else:
                st.error("Invalid username or password. Please try again.")

# Main Page Content
if st.session_state.authenticated or st.session_state.authenticated_plus:
    # Handling Logout Immediately
    if selected == "Log Out":
        # Clear the authentication status
        st.session_state.authenticated = False
        st.session_state.authenticated_plus = False
        # Display a success message
        st.success("You have been logged out.")
        # Immediately rerun the script to reflect the logout status
        st.rerun()
    else:
        render_page(selected)
else:
    render_page(selected)
