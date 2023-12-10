import streamlit as st

def center_success_message(message):
    st.markdown(
        f"""
        <div style="
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        ">
            <div style="
                background-color: #00cc00;
                color: white;
                padding: 20px;
                border-radius: 5px;
                text-align: center;
            ">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    st.title("Custom Success Message")

    # Button to trigger success message
    if st.button("Show Success Message"):
        center_success_message("Operation successful!")

if __name__ == "__main__":
    main()
