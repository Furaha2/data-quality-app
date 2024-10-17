# Here is where the framework will be displayed
# Provide a place for feedback/comments
# look at Analytics to see how many times the page is viewed
# could read report from Google Drive.
import streamlit as st

# importing function set_menu from streamlit.py to create menu in all pages
from streamlit_app import set_menu
import streamlit.components.v1 as components

set_menu()

path_to_intro = "./framework_report.html" 
path_to_method = "./dq_methodology.html"
path_to_results = "./results.html"

with open(path_to_intro,'r') as f: 
    intro_html = f.read()

with open(path_to_method,'r') as f: 
    method_html = f.read()

with open(path_to_results,'r') as f: 
    results_html = f.read()

# Show in webpage
st.markdown(intro_html, unsafe_allow_html=True)
# st.markdown(method_html, unsafe_allow_html=True)
# st.markdown(results_html, unsafe_allow_html=True)

# read full report
st.link_button("Read full report", "https://streamlit.io/gallery")

# to do:
# write a summary of the report and include a link to redirect to the full report
# save DQ framework report as pdf on google drive and include link to read full report btn