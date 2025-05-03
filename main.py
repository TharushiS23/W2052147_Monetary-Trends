import streamlit as st
from loading import show_loading_game
from app import main  # assuming your dashboard is also in app.py (see note below)

# Run app or game based on session state
if 'appcode' not in st.session_state:
    st.session_state['appcode'] = False

if st.session_state['appcode']:
    main()
else:
    show_loading_game()