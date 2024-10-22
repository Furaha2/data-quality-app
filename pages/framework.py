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

with open(path_to_intro,'r') as f: 
    intro_html = f.read()

# Show in webpage
st.markdown(intro_html, unsafe_allow_html=True)

# read full report
st.link_button("Read full report", "https://docs.google.com/document/d/12qNWaTqQciBgz9-kfHVT0nXsaKQgI428j8ZHHel885g/edit#heading=h.1pdl8nz2j1ee")
