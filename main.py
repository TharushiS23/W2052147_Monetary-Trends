import streamlit as st
import os
import sys

# Check what page to load based on URL path
def main():
    # Get the file path
    current_path = os.path.basename(sys.argv[0])
    
    # Default page is loading page
    import loading
    loading.main()

if __name__ == "__main__":
    main()