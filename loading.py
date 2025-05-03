import streamlit as st
import os
from streamlit.components.v1 import html
import time

# Page config
st.set_page_config(
    page_title="Loading Page",
    page_icon="⌛",
    layout="wide"
)

# Custom CSS to style the page
st.markdown("""
<style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #1E88E5;
        color: white;
        font-size: 1.2rem;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        border: none;
        margin: 0 auto;
        display: block;
    }
    .stButton > button:hover {
        background-color: #1565C0;
    }
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    .game-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Title and subtitle
    st.markdown('<div class="main-title">Welcome to the Monetary Trends Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Enjoy a game of Sudoku while the dashboard loads</div>', unsafe_allow_html=True)
    
    # Create columns for layout
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Embed the Sudoku game using an iframe
        st.markdown('<div class="game-container">', unsafe_allow_html=True)
        html("""
            <iframe src="http://www.free-sudoku.com/sudoku-webmaster.php" 
                    width="500" 
                    height="562" 
                    frameborder="0"
                    style="margin: 0 auto; display: block;">
            </iframe>
        """, height=580)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Button to open main app
    if st.button('Launch Main Dashboard'):
        # Use session state to indicate we should load the main app content
        st.session_state.show_main_dashboard = True
        st.rerun()
    
    # Check if we should show the main dashboard
    if 'show_main_dashboard' in st.session_state and st.session_state.show_main_dashboard:
        # Import and run the main app code
        import app
        app.main()

if __name__ == "__main__":
    main()