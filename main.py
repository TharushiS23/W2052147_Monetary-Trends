import streamlit as st
import os

# Initialize session state
if 'show_main_dashboard' not in st.session_state:
    st.session_state.show_main_dashboard = False

# Main entry point
def main():
    # Import loading page first
    import loading
    loading.main()

if __name__ == "__main__":
    main()