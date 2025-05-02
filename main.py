import streamlit as st

# Initialize session state
if 'Main_app' not in st.session_state:
    st.session_state['Main_app'] = False

# Determine which page to show
if st.session_state['Main_app']:
    # Import and run your existing dashboard
    import app
    app.main()  # This runs your existing dashboard code
else:
    # Import and run the game/loading page
    from loadingpage import loading_page
    loading_page()