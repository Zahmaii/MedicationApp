import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
from matplotlib.colors import LinearSegmentedColormap

# Import the All Different Pages
from scan_page import scanning_page
from premium_page import render_premium_page

# Set Up Login Variables
premium_credentials = {
    "prime": "password",
}
premium_plus_credentials = {
    "elite": "password_pls",
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
        # if selected == "Scan":
        #     scanning_page() # Calling Scanning Page 
        # elif selected == "Search":
        #     scanning_page() # Calling Search Page

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
        render_premium_page()  # Calling Premium Page File
    
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
                st.session_state.username = username
                st.success("Login successful!")
                login_placeholder.empty()  # Remove the login form immediately
            elif auth_status == "authenticated_plus":
                st.session_state.authenticated_plus = True
                st.session_state.username = username
                st.success("Premium Plus login successful!")
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

