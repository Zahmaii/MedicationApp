import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
from matplotlib.colors import LinearSegmentedColormap
from streamlit_webrtc import webrtc_streamer  # Ensure this is imported for webcam streaming

# Load the datasets (adjust the paths if needed)
try:
    df1 = pd.read_csv('medications_1.csv')  # Original dataset
    df2 = pd.read_csv('medications_2.csv')  # New dataset
except Exception as e:
    st.error(f"Error loading the datasets: {e}")
    df1 = None
    df2 = None

# Function for searching medications in both datasets
def search_medication(med_name):
    if df1 is not None and 'Drug Name' in df1.columns:
        df1_results = df1[df1['Drug Name'].str.contains(med_name, case=False, na=False)]
    else:
        df1_results = pd.DataFrame()

    if df2 is not None and 'Drug Name' in df2.columns:
        df2_results = df2[df2['Drug Name'].str.contains(med_name, case=False, na=False)]
    else:
        df2_results = pd.DataFrame()

    # Combine results from both datasets
    combined_results = pd.concat([df1_results, df2_results]).drop_duplicates().reset_index(drop=True)
    return combined_results

# Function to display medication details
def display_medication_options(search_results):
    if not search_results.empty:
        selected_med = st.selectbox("Select the specific medication:", search_results['Drug Name'].unique(), key="med_select")
        if selected_med:
            # Check which dataset the medication is in and display the details
            if selected_med in df1['Drug Name'].values:
                specific_med = df1[df1['Drug Name'] == selected_med].iloc[0]
            else:
                specific_med = df2[df2['Drug Name'] == selected_med].iloc[0]

            st.write(f"### Medication Name: {specific_med['Drug Name']}")
            st.write(f"**Therapeutic Class:** {specific_med['Therapeutic Class']}")
            st.write(f"**Description:** {specific_med['use0']}")
            st.write(f"**Side Effects:** {specific_med['sideEffect0']}")
            # st.write(f"**Active Ingredients:** {specific_med['Active Ingredients']}")
    else:
        st.write("No medication found.")

# Function to handle video frame callback (webcam feed processing)
def video_frame_callback(frame):
    # Convert frame to RGB
    img = frame.to_image()
    img = np.array(img)
    
    # Apply medication detection on the image
    if df1 is not None:
        detected_name = df1['Drug Name'].iloc[0]  # For now, return the first medication
        
        # Check if the detected name is in the second dataset as well
        if detected_name in df2['Drug Name'].values:
            st.write(f"### Detected Medication: {detected_name} (Found in both datasets)")
        else:
            st.write(f"### Detected Medication: {detected_name} (Found in first dataset only)")

    # Convert image back to format streamlit_webrtc expects
    return frame

# Set Up Login Variables
premium_credentials = {
    "prime": "primepass",
}
premium_plus_credentials = {
    "elite": "elitepass",
}

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
            if df1 is not None or df2 is not None:
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
                        # Make sure to check both datasets
                        if detected_name in df1['Drug Name'].values:
                            medication_info = df1[df1['Drug Name'] == detected_name].iloc[0]
                        elif detected_name in df2['Drug Name'].values:
                            medication_info = df2[df2['Drug Name'] == detected_name].iloc[0]

                        st.write(f"### Medication Info: ")
                        st.write(f"**Drug Name**: {medication_info['Drug Name']}")
                        st.write(f"**Drug Class**: {medication_info['Drug Class']}")
                        st.write(f"**Description**: {medication_info['Description']}")
                        st.write(f"**Side Effects**: {medication_info['Side Effects']}")
                        st.write(f"**Active Ingredients**: {medication_info['Active Ingredients']}")

        elif selected == "Search":
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
