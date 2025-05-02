import streamlit as st
import loadingpage  # Your loading page module
import app

# Initialize session state safely
if 'app' not in st.session_state:
    st.session_state['app'] = False  # or True, depending on your logic

if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

def main():

    # Determine which page to show
    if st.session_state['app']:
        loadingpage.run_loading_page()
    else:
        app.main()

if __name__ == "__main__":
    main()
