import streamlit as st

def show_loading_game():
    st.title("🧩 Play Sudoku")

    # Embed the external Sudoku game using HTML iframe
    st.components.v1.html(
        """
        <iframe src="http://www.free-sudoku.com/sudoku-webmaster.php" 
                width="100%" 
                height="600" 
                frameborder="0" 
                scrolling="no">
        </iframe>
        """,
        height=600,
    )

    # Go to Main App button
    if st.button("🚀 Go to Main App"):
        st.session_state['appcode'] = True
        if "Player_pos" in st.session_state:
            del st.session_state.player_pos
        st.rerun()