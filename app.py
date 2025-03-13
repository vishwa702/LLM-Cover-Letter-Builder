import streamlit as st


pages = {
    "Navigation": [
        st.Page("pages/Resume_Builder.py", title="Resume Builder"),
        st.Page("pages/File_Management.py", title="File Management"),
    ],

}

pg = st.navigation(pages)
pg.run()