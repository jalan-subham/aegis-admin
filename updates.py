import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os

SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def main():
    st.markdown("<h1 class='centered'>Updates: </h1>", unsafe_allow_html=True)
    # Button to redirect to the upload page
    if st.button("Go to Upload Page"):
        # Update the session state to change the current page
        st.session_state.current_page = "upload"
        # Trigger a rerun to render the new page
        st.experimental_rerun()
    with st.form("date_form"):
        date = st.date_input("Enter date: ")
        submit_button = st.form_submit_button(label='Submit')
    if submit_button:
    
        tasks = supabase.table('tasks').select("*, personnel_list(rank, guard_clock)").eq('task_date', date).execute().data
        if len(tasks) == 0:
            st.write("No records found")
        else:
            for i in range(len(tasks)):
                tasks[i]["Rank"] = tasks[i]["personnel_list"]["rank"]
                tasks[i]["Clock No"] = tasks[i]["personnel_list"]["guard_clock"]
                del tasks[i]["personnel_list"]
            df = pd.DataFrame(tasks)
            st.markdown(f"### {date}")
            df = df.drop(columns=['id','task_date','created_at','location'])
            df['S No'] = range(1, len(df) + 1)
            new_column_names = {'shift': 'Shift','name': 'Name','completed':'Status','Rank':'Rank','Clock No': 'Clock No', 'S No':'S No', "task_type": "Task Type"}
            df.rename(columns=new_column_names, inplace=True)
            desired_columns_order = ['S No', 'Clock No', 'Rank', 'Name', "Task Type", 'Shift', 'Status']
            df = df[desired_columns_order]
            st.write(df)

if __name__ == "__main__":
    main()