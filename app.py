import streamlit as st


pages = {
    "Navigation": [
        st.Page("pages/Resume_Builder.py", title="Resume Builder", icon=':material/rocket_launch:'),
        st.Page("pages/File_Management.py", title="File Management", icon=':material/folder:'),
    ],

}

pg = st.navigation(pages)
pg.run()