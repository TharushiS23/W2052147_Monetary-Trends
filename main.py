import streamlit as st
from loading import show_loading_game
from dashboard import main  

# Run app or game based on session state
if 'appcode' not in st.session_state:
    st.session_state['appcode'] = False

if st.session_state['appcode']:
    main()
else:
    show_loading_game()