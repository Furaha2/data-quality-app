# gives a report on the quality of data

import streamlit as st

# importing function set_menu from streamlit.py to create menu in all pages
from streamlit_app import set_menu
set_menu()

st.header('Dataset Quality Checks')

# to do:
# print words that define each dimension evaluated
# and interpret the meaning of the scores
# persist streamlit app page

if 'df_scores' in st.session_state:
    file_name = st.session_state['file_name']
    st.write(file_name)
    df_scores = st.session_state['df_scores']
    styled_df = df_scores.style.hide()
    st.write(styled_df.to_html(), unsafe_allow_html=True)