import streamlit as st
import time

# Loading page with embedded Puzzle Game
def loading_game():
    # Customizing the title of the page
    st.set_page_config(page_title="Loading Page", page_icon="🧩")

    # Header for loading screen
    st.markdown("<h1 style='text-align: center;'>🧩 Enjoy a quick Sudoku!</h1>", unsafe_allow_html=True)

    # Embed the external Puzzle game using an iframe
    st.markdown("""
        <iframe src="http://www.free-sudoku.com/sudoku-webmaster.php" width="500" height="562" frameborder="0"></iframe>
    """, unsafe_allow_html=True)

    # Simulate loading process
    with st.spinner("Preparing your dashboard... Please wait!"):
        time.sleep(3)  # Adjust to however long you want your "loading" to appear

    # After the loading process, show a message and give the option to go to the dashboard
    st.success("Dashboard is ready!")

    # Go to Main App button
    if st.button("Main App"):
        st.session_state['app'] = True
        if "Player_pos" in st.session_state:
            del st.session_state.player_pos
        st.rerun()

