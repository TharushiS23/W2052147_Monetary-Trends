import streamlit as st

# Initialize session state
if 'appcode' not in st.session_state:
    st.session_state['appcode'] = False

# Determine which page to show
if st.session_state['appcode']:
    # Import and run your existing dashboard
    import app
    app.main()  # This runs your existing dashboard code
else:
    # Import and run the game/loading page
    from loadingpage import show_loading_game
    show_loading_game()