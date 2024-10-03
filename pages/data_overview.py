# shows data overview
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_ydata_profiling import st_profile_report

if 'pr' in st.session_state:
    # data_overview = st.session_state['dt_overview']
    # st.write(st.session_state['dt_overview'])
    st_profile_report(st.session_state['pr'], navbar=True)