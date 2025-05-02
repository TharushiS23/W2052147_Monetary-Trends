import streamlit as st
import time

# Loading page with embedded Snake and Ladders Game
def loading_page():
    # Customizing the title of the page
    st.set_page_config(page_title="Loading Page", page_icon="🎲")

    # Header for loading screen
    st.markdown("<h1 style='text-align: center;'>🎲 Loading... Play Snake & Ladders While We Prepare Your Dashboard</h1>", unsafe_allow_html=True)

    # Embed the external Snake and Ladders game using an iframe
    st.markdown("""
        <iframe src="https://www.playsnakeandladder.com" width="100%" height="600px"></iframe>
    """, unsafe_allow_html=True)

    # Simulate loading process
    with st.spinner("Preparing your dashboard... Please wait!"):
        time.sleep(5)  # Adjust the time you want for "loading"

    # After the loading process, show a message and give the option to go to the dashboard
    st.success("🎉 Dashboard is ready!")

    # Give the user the option to go to the main dashboard anytime
    if st.button("Go to Dashboard"):
        st.experimental_rerun()  # This will reload the page and transition to the main app

if __name__ == "__main__":
    loading_page()