import streamlit as st
from check import render_login_page, render_updates_page
from updates import main as updates_main
from upload import main as upload_main

# Initialize session state to store navigation state and user login status
session_state = st.session_state
if 'is_logged_in' not in session_state:
    session_state.is_logged_in = False
if 'current_page' not in session_state:
    session_state.current_page = 'login'

# Main app logic
if not session_state.is_logged_in:
    render_login_page()
elif session_state.is_logged_in:
    if session_state.current_page == "upload":
        upload_main()  # Render the upload page
    else:
        render_updates_page()  # Render the updates page
