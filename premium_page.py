import streamlit as st

def render_premium_page():
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
