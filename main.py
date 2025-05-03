import streamlit as st
import os

# Set page config at the very beginning
st.set_page_config(
    page_title="Monetary Trends Dashboard",
    page_icon="⌛",
    layout="wide"
)

# Initialize session state
if 'show_main_dashboard' not in st.session_state:
    st.session_state.show_main_dashboard = False

# Main entry point
def main():
    if st.session_state.show_main_dashboard:
        # Import and run the dashboard when requested
        import app
        app.main()
    else:
        # Import and run loading screen
        import loading
        loading.main()

if __name__ == "__main__":
    main()