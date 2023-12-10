import streamlit as st
import pandas as pd
from updates import main as updates_main  # Import the updates page

# Initialize session state to store navigation state and user login status
session_state = st.session_state
if 'is_logged_in' not in session_state:
    session_state.is_logged_in = False

# Function to render the login page
def render_login_page():
    st.markdown("<h1 class='centered'>Welcome to Project Aegis!</h1>", unsafe_allow_html=True)

    # Resize and display the logo
    logo_path = "logo2.png"  # Adjust the path to your logo file
    st.image(logo_path, width=150, use_column_width=False)

    # Read Excel file and extract usernames (clock numbers)
    file_path = 'guard_details.xlsx'

    try:
        df = pd.read_excel(file_path, skiprows=2)
        filtered_df = df[df['Rank'].isin(['SECURITY SUPERVISOR', 'SECURITY OFFICER'])]

        if not filtered_df.empty:
            clock_numbers = filtered_df['Clock No'].astype(str).tolist()

            # User Input: Username
            username_key = "username_input"  # Add a unique key identifier
            username = st.text_input("Username", key=username_key)

            # User Input: Password
            password_key = "password_input"  # Add a unique key identifier
            password = st.text_input("Password", type="password", key=password_key)

            # Login Button
            if st.button("Login"):
                # Check if the entered username and password are valid
                if username in clock_numbers and password == "aegis@123":
                    st.success("Login Successful!")

                    # Update session state to indicate user is logged in
                    session_state.is_logged_in = True

                    # Use st.experimental_set_query_params for immediate redirection
                    st.experimental_set_query_params(logged_in=True)
                    st.experimental_rerun()

                else:
                    st.error("Invalid Username or Password. Try again.")

        else:
            st.warning("No matching entries found in the database.")

    except FileNotFoundError:
        st.error(f"Error: File '{file_path}' not found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Function to render the updates page
def render_updates_page():
    updates_main()
