import streamlit as st
import pandas as pd
import numpy as np 
import json
from supabase import create_client, Client
import time
import os
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def process_data(file_path):
    df = pd.read_excel(file_path, skiprows=2)
    df = df.replace({np.nan: None})
    df = df[df['SHIFT'] != 'L']
    sorting_order = {
        'SECURITY SUPERVISOR': 1,
        'HEAD GUARD': 2,
        'SECURITY GUARD': 3,
        'CCTV': 4,
        'LADY SECURITY GUARD': 5
    }
    df['Rank'] = df['Rank'].replace(sorting_order)
    df['Clock No'] = df['Clock No'].astype(str)
    df = df.sort_values(by=['SHIFT', 'Rank'], ascending=[True, True])
    reverse_sorting_order = {v: k for k, v in sorting_order.items()}
    df['Rank'] = df['Rank'].replace(reverse_sorting_order)
    df['S No'] = range(1, len(df) + 1)
    return df

def row_to_dict(row, task_date):
    return {
        'shift': row['SHIFT'],
        'name': row['NAME'],
        'task_type': row['TASK'],
        'location': row['LOCATION'],
        'task_date': task_date
    }

def show_popup(message, duration=1.5):
    popup = st.markdown(
        f'<div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); padding: 20px; background-color: #4CAF50; color: white; border-radius: 5px; z-index: 999;">{message}</div>',
        unsafe_allow_html=True
    )
    time.sleep(duration)
    popup.empty()


def main():
    st.title(" Upload: ")
    upload_text = st.empty()
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"], accept_multiple_files=False)

    # Button to redirect to the updates page
    if st.button("Go to Updates Page"):
        st.session_state.current_page = 'updates'  # Set the current page to 'updates'
        st.experimental_rerun()

    if uploaded_file is not None:
        try:
            # Get the list of sheet names in the Excel file
            xl_file = pd.ExcelFile(uploaded_file)
            sheet_names = xl_file.sheet_names
            # Allow the user to select a sheet using a selectbox
            selected_sheet = st.selectbox("Select a sheet:", sheet_names)
            # Process the uploaded data
            
            df_processed = process_data(uploaded_file)
            # st.write("Processed Data:")
            st.write(df_processed)  # Display the processed DataFrame
            show_popup("Uploaded successfully!")
            # st.success("File sent!")

            # Extract file name without extension
            task_date = os.path.splitext(os.path.basename(uploaded_file.name))[0]
            processed_data = process_data(uploaded_file)
            upload_text.subheader("Uploading Data...")
            for index, row in processed_data.iterrows():
                row_dict = row_to_dict(row, task_date)
                print(type(row_dict["location"]))
                data, count = supabase.table("tasks").insert(json.loads(json.dumps(row_dict))).execute()
        
            upload_text.empty()
            upload_text.subheader("Upload successful!")
        except Exception as e:
            pass
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()