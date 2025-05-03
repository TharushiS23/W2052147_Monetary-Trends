import streamlit as st

# Initialize session state
if 'dashboard' not in st.session_state:
    st.session_state['dashboard'] = False

# Determine which page to show
if st.session_state['dashboard']:
    # Import and run your existing dashboard
    import dashboard
    dashboard.main()  # This runs your existing dashboard code
else:
    # Import and run the game/loading page
    from loading_game import show_loading_game
    show_loading_game()