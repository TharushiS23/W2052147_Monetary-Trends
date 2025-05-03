import streamlit as st
import random

# Word list for the game
word_list = [
    "function", "loop", "array", "string", "integer",
    "boolean", "variable", "class", "object", "method",
    "list", "return", "print", "compile", "debug",
    "import", "export", "value", "constant", "operator",
    "exception", "error", "condition", "input", "output",
    "logic", "recursion", "index", "argument", "parameter"
]

# Function to get a new scrambled word
def get_new_scrambled_word():
    word = random.choice(word_list)
    scrambled = ''.join(random.sample(word, len(word)))
    while scrambled == word:
        scrambled = ''.join(random.sample(word, len(word)))
    return word, scrambled

def show_loading_game():
    st.title("🔤 Scrambled Word Game")

    # Initialize state variables
    if "original_word" not in st.session_state:
        st.session_state.original_word, st.session_state.scrambled_word = get_new_scrambled_word()
        st.session_state.score = 0
        st.session_state.last_result = ""
    
    # Display scrambled word
    st.markdown(f"**Guess this word:** `{st.session_state.scrambled_word}`")
    
    # Input for guess
    guess = st.text_input("Your guess:", key="guess_input")
    
    # Check guess
    if st.button("Submit"):
        if guess.strip().lower() == st.session_state.original_word:
            st.session_state.score += 1
            st.session_state.last_result = "✅ Correct!"
        else:
            st.session_state.last_result = f"❌ Incorrect! The correct word was **{st.session_state.original_word}**."
        # Get a new word for the next round
        st.session_state.original_word, st.session_state.scrambled_word = get_new_scrambled_word()
        st.rerun()

    # Show last result and score
    if st.session_state.last_result:
        st.info(st.session_state.last_result)
    st.write(f"🏆 Score: {st.session_state.score}")

    # Go to Main App button
    if st.button("🚀 Go to Main App"):
        st.session_state['dashboard'] = True
        if "Player_pos" in st.session_state:
            del st.session_state.player_pos
        st.rerun()
