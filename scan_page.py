import pandas as pd
import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit_webrtc import webrtc_streamer
import time

# Load the dataset (adjust the path if needed)
def load_medication_data():
    try:
        # Load dataset from CSV file
        df = pd.read_csv('medications.csv')  # Path to your CSV file
        return df
    except Exception as e:
        st.error(f"Error loading the dataset: {e}")
        return None

# Function to search for medication in the dataset
def get_medication_info(medication_name, df):
    # Search for medication in the dataset
    medication_info = df[df['Drug Name'].str.contains(medication_name, case=False, na=False)]
    
    if medication_info.empty:
        return None
    else:
        return medication_info.iloc[0]

# Function to detect medication via webcam (basic example)
def detect_medication(image, model):
    # This should be where you use your model to detect medications.
    # For demonstration, we will return a random medication from the dataset.
    df = load_medication_data()
    if df is not None:
        return df['Drug Name'].iloc[0]  # Return the first medication for now
    return None

# Function to display webcam feed
def video_frame_callback(frame):
    # Convert frame to RGB
    img = frame.to_image()
    img = np.array(img)
    
    # Apply medication detection on the image
    detected_name = detect_medication(img, model=None)  # Replace 'model' with your object detection model

    # Display the detected medication name below the image
    if detected_name:
        st.write(f"### Detected Medication: {detected_name}")
        
    # Convert image back to format streamlit_webrtc expects
    return frame

# Scanning Page Code
def scanning_page():
    st.write("Use your camera to scan medication.")
    
    # Load dataset
    df = load_medication_data()

    if df is not None:
        # Use webcam stream with streamlit_webrtc
        webrtc_ctx = webrtc_streamer(
            key="example", 
            video_frame_callback=video_frame_callback,
            media_stream_constraints={"video": True, "audio": False},
            video_html_attrs={"width": "100%"}
        )

        # Display the detected medication below the webcam feed
        if webrtc_ctx.video_frame_callback:
            detected_name = webrtc_ctx.video_frame_callback(None)  # This will run detection logic
            if detected_name:
                medication_info = get_medication_info(detected_name, df)
                if medication_info is not None:
                    st.write(f"### Medication Info:")
                    st.write(f"**Drug Name**: {medication_info['Drug Name']}")
                    st.write(f"**Drug Class**: {medication_info['Drug Class']}")
                    st.write(f"**Description**: {medication_info['Description']}")
                    st.write(f"**Side Effects**: {medication_info['Side Effects']}")
                    st.write(f"**Active Ingredients**: {medication_info['Active Ingredients']}")
