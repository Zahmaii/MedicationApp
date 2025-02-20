import numpy as np
import pandas as pd
import streamlit as st
import datetime
import tempfile
import time
import random
from fpdf import FPDF
from streamlit_option_menu import option_menu
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
            st.write("Use your camera to scan medication.")
            
            if df1 is not None or df2 is not None:
                webrtc_ctx = webrtc_streamer(
                    key="example", 
                    video_frame_callback=video_frame_callback,
                    media_stream_constraints={"video": True, "audio": False},
                    video_html_attrs={"width": "100%"}
                )

                if webrtc_ctx and webrtc_ctx.state.playing:
                    detected_name = video_frame_callback(None)  
                    if detected_name:
                        if detected_name in df1['Drug Name'].values:
                            medication_info = df1[df1['Drug Name'] == detected_name].iloc[0]
                        elif detected_name in df2['Drug Name'].values:
                            medication_info = df2[df2['Drug Name'] == detected_name].iloc[0]

                        st.session_state.searched_medication = medication_info  # Save scanned medication info

                        st.write(f"### Medication Info: ")
                        st.write(f"**Drug Name**: {medication_info['Drug Name']}")
                        st.write(f"**Therapeutic Class**: {medication_info['Therapeutic Class']}")
                        st.write(f"**Side Effects 1**: {medication_info['sideEffect0']}")
                        st.write(f"**Side Effects 2**: {medication_info['sideEffect1']}")
                        st.write(f"**Side Effects 3**: {medication_info['sideEffect2']}")
                        st.write(f"**Description**: {medication_info['use0']}")

        elif selected == "Search":
            st.title("Search Medication")
            search_query = st.text_input("Enter Medication Name:", key="search_query").strip()
            if search_query:
                search_results = search_medication(search_query)
                display_medication_options(search_results)
                
                if not search_results.empty:
                    medication_info = search_results.iloc[0]
                    st.session_state.searched_medication = medication_info  # Save searched medication info
                    
                    st.write(f"### Medication Info: ")
                    st.write(f"**Drug Name**: {medication_info['Drug Name']}")
                    st.write(f"**Therapeutic Class**: {medication_info['Therapeutic Class']}")
                    st.write(f"**Side Effects 1**: {medication_info['sideEffect0']}")
                    st.write(f"**Side Effects 2**: {medication_info['sideEffect1']}")
                    st.write(f"**Side Effects 3**: {medication_info['sideEffect2']}")
                    st.write(f"**Description**: {medication_info['use0']}")

    elif selected == "Management":
        st.title("Medication Management")
        
        if "searched_medication" in st.session_state and st.session_state["searched_medication"] is not None:
            # If a medication has been searched, display its details
            st.write(f"Managing: **{st.session_state.searched_medication['Drug Name']}**")
            st.write("-"*50)
            
            st.subheader("Medication Inventory")
            if "medication_inventory" not in st.session_state:
                st.session_state.medication_inventory = []
            
            med_name = st.text_input("Medication Name:")
            med_qty = st.number_input("Quantity Available:", min_value=0, step=1)
            if st.button("Add Medication"):
                st.session_state.medication_inventory.append({"name": med_name, "quantity": med_qty})
                st.success(f"Added {med_name} to inventory.")
            
            if st.session_state.medication_inventory:
                st.table(st.session_state.medication_inventory)
            
            st.write("-"*50)
            st.subheader("Set Medication Reminder")
            reminder_med = st.selectbox("Select Medication:", [m["name"] for m in st.session_state.medication_inventory])

            # Input for first dose time and dose interval
            first_dose_time = st.time_input("First Dose Time:")
            dose_interval = st.number_input("Dose Interval (hours):", min_value=4, step=1)

            # If dose interval is less than 4, display error and don't generate the table or chart
            if dose_interval >= 4:
                # Button to set reminder
                if st.button("Set Reminder"):
                    next_dose = datetime.datetime.combine(datetime.date.today(), first_dose_time) + datetime.timedelta(hours=dose_interval)
                    
                    # Save the reminder in session state
                    if "medication_reminders" not in st.session_state:
                        st.session_state["medication_reminders"] = []

                    # Add the reminder to the list
                    st.session_state["medication_reminders"].append({
                        "medication": reminder_med,  # Ensure this key is consistent
                        "first_dose_time": first_dose_time,
                        "next_dose_time": next_dose.time()
                    })

                    # Display reminders in a table
                    reminder_df = pd.DataFrame(st.session_state["medication_reminders"])
                    st.table(reminder_df)

                    # Add chart generation code here if needed (only after dose_interval check)
                    # Example chart (optional):
                    # st.line_chart(reminder_df["next_dose_time"])
            else:
                st.error("Please enter a dose interval of at least 4 hours.")
        
        else:
            # If no medication is searched, just show the current time
            st.write("No medication selected. Please scan or search for medication.")
            
            # Display current time
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.write(f"Current Time: {current_time}")

    elif selected == "History":
        st.title("History Page")
        st.write("View past medication searches, reminders, and orders.")
        
        # Display previously searched medication
        if "searched_medication" in st.session_state and st.session_state["searched_medication"] is not None:
            st.write(f"Previously searched medication: **{st.session_state.searched_medication['Drug Name']}**")
            st.write("-"*50)
        else:
            st.write("No medication has been searched yet.")
        
        # Display previously set reminders
        if "medication_reminders" in st.session_state and st.session_state["medication_reminders"]:
            st.subheader("Reminder History")
            
            for reminder in st.session_state["medication_reminders"]:
                # Use .get() to avoid KeyError in case the key is missing
                medication = reminder.get("medication", "N/A")
                first_dose_time = reminder.get("first_dose_time", "N/A")
                next_dose_time = reminder.get("next_dose_time", "N/A")

                st.write(f"Medication: **{medication}** - First Dose: {first_dose_time} - Next Dose: {next_dose_time}")
        else:
            st.write("No reminders have been set yet.")
        
        # Display order history (if any)
        if "order_history" in st.session_state and st.session_state["order_history"]:
            st.write("-"*50)
            st.subheader("Order History")
            for order in st.session_state["order_history"]:
                st.write(f"Order Date: {order['order_date']} - Item: {order['item']} - Quantity: {order['quantity']} - Total Cost: ${order['total_cost']:.2f}")
        else:
            st.write("No orders have been placed yet.")

    elif selected == "Delivery":
        st.title("Delivery Page")

        # Automatically use the medication name from the scanned data if available
        medication_name = ""
        if "searched_medication" in st.session_state and st.session_state["searched_medication"] is not None:
            medication_name = st.session_state.searched_medication['Drug Name']

        # Order Form
        with st.form("order_form"):
            st.subheader("Place Your Order")
            st.write(f"Selected Medication: **{medication_name}**")
            quantity = st.number_input("Quantity", min_value=1, step=1, value=1)
            uploaded_file = st.file_uploader("Upload Prescription (PDF, JPG, PNG)", type=["pdf", "jpg", "png"])
            submitted = st.form_submit_button("Place Order")

        if submitted:
            if uploaded_file:
                st.write("Processing Order...")
                progress_bar = st.progress(0)  # Initialize progress bar

                for i in range(100):  
                    time.sleep(0.03)  # Simulate processing time
                    progress_bar.progress(i + 1)  # Update progress bar

                st.write("Process Completed!")
                st.write("-"*50)

                # Random cost per unit (between 5 and 50)
                cost_per_unit = random.randint(5, 50)
                medication_cost = cost_per_unit * quantity  # Total cost for medication
                delivery_cost = 5  # Fixed delivery cost
                total_cost = medication_cost + delivery_cost  # Total cost
                
                st.markdown("**Order Summary**")
                # Create order data for table
                order_data = {
                    "Name": [medication_name, "Delivery"],
                    "Quantity": [quantity, "-"],  # Delivery doesn't have quantity
                    "Cost per Unit": [f"${cost_per_unit:.2f}", "-"],  # Delivery cost doesn't have unit price
                    "Delivery Cost": ["-", f"${delivery_cost:.2f}"],
                    "Total Cost": [f"${medication_cost:.2f}", f"${total_cost:.2f}"]
                }

                # Display the order data as a table
                order_df = pd.DataFrame(order_data)
                st.table(order_df)

                # Display total cost
                st.write(f"**Total Cost: ${total_cost:.2f}**")
                st.success("Order placed successfully!")

                # Save order history in session state
                if "order_history" not in st.session_state:
                    st.session_state.order_history = []

                st.session_state.order_history.append({
                    "order_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "item": "Medication",
                    "quantity": quantity,
                    "total_cost": total_cost
                })
                
                # Generate PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, "Order Receipt\n\n" + order_df.to_string(index=False))
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                pdf.output(temp_file.name)

                # Download button
                with open(temp_file.name, "rb") as file:
                    st.download_button("Download Receipt", file, "order_receipt.pdf", mime="application/pdf")
            else:
                st.error("Please upload a prescription to proceed.")

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
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Type of Premium", value="Prime")
        col2.metric(label="Price (Monthly)", value="$15")
        col3.metric(label="Price (Yearly)", value="$150")
        st.write("### Features of Prime:")
        prime_features = [
            "✔️ History",
            "✔️ Delivery"
        ]
        st.write("\n".join(prime_features))
        # st.markdown('<button class="premium-button">Purchase Prime</button>', unsafe_allow_html=True)
        # st.markdown('</div>', unsafe_allow_html=True)

        # Elite Version
        st.write("-"*75)
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Type of Premium", value="Elite")
        col2.metric(label="Price (Monthly)", value="$20")
        col3.metric(label="Price (Yearly)", value="$200")
        st.write("### Features of Elite:")
        elite_features = [
            "🌟 History",
            "🌟 Schedule Delivery",
            "🌟 Family Plan"
        ]
        st.write("\n".join(elite_features))
        # st.markdown('<button class="premium-button">Purchase Elite</button>', unsafe_allow_html=True)
        # st.markdown('</div>', unsafe_allow_html=True)

        # Reminder for Premium Plus
        st.markdown("""
            <div style="font-size: 18px; text-align: center; color: #7F8C8D; margin-top: 40px;">
                Upgrade to Elite for the ultimate experience and exclusive benefits!
            </div>
        """, unsafe_allow_html=True)
        
    elif selected == "Family Plan":
        st.title("Family Plan")
        st.write("Manage your family's medication tracking.")

        # Initialize the family members list if not already initialized
        if "family_members" not in st.session_state:
            st.session_state.family_members = []

        # Add family members if less than 5
        if len(st.session_state.family_members) < 5:
            with st.form("add_family_member"):
                family_name = st.text_input("Family Member Name:")
                family_age = st.number_input("Age:", min_value=0, step=1)
                family_relation = st.text_input("Relationship:")
                submitted = st.form_submit_button("Add Family Member")
                if submitted:
                    st.session_state.family_members.append({"Name": family_name, "Age": family_age, "Relationship": family_relation})
                    st.success(f"Added {family_name} to the family plan.")
        else:
            st.error("You have reached the limit of 5 family members.")
        
        # Display family members in a table format
        if st.session_state.family_members:
            # Create a DataFrame for easier display
            family_df = pd.DataFrame(st.session_state.family_members)

            # Add a column for the delete emoji (🗑️)
            family_df["Remove"] = family_df.apply(lambda x: "🗑️", axis=1)
            
            # Display the table with the delete button in the last column
            for index, member in family_df.iterrows():
                # Display each row with a delete button
                cols = st.columns([3, 2, 2, 1])  # Adjust the column width as needed
                
                # Display family member info in columns
                cols[0].write(f"**{member['Name']}**")
                cols[1].write(f"Age: {member['Age']}")
                cols[2].write(f"Relationship: {member['Relationship']}")
                delete_button = cols[3].button("🗑️", key=f"remove_{index}")
                
                if delete_button:
                    # Remove the selected family member from the session state
                    st.session_state.family_members.pop(index)
                    st.success(f"Removed {member['Name']} from the family plan.")
                    st.rerun()  # Re-render the page after deletion

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
