import streamlit as st


pages = {
    "Navigation": [
        st.Page("pages/1_Resume_Builder.py", title="Cover Letter Builder", icon=':material/rocket_launch:'),
        st.Page("pages/2_File_Management.py", title="File Management", icon=':material/folder:'),
    ],

}

pg = st.navigation(pages)
pg.run()