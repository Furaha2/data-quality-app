# gives a report on the quality of data

import streamlit as st

st.header('Dataset Quality Checks')

# to do:
# print words that define each dimension evaluated
# and interpret the meaning of the scores
# print the file name
# persist streamlit app page
# change file names

if 'df_scores' in st.session_state:
    file_name = st.session_state['file_name']
    st.write(file_name)
    # description = file_name.join('You are viewing')
    df_scores = st.session_state['df_scores']
    styled_df = df_scores.style.hide()
    st.write(styled_df.to_html(), unsafe_allow_html=True)