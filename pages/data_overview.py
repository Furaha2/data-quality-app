# shows data overview
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report
import pandas as pd

# importing function set_menu from streamlit.py to create menu in all pages
from streamlit_app import set_menu
set_menu()

if 'pr' in st.session_state:
    st_profile_report(st.session_state['pr'], navbar=True)
    df = st.session_state['df']
    st.write('Dataframe top 5 rows (Hover on table to see expand icon)')
    st.write(df.head())