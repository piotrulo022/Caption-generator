import streamlit as st
from base64 import b64encode 

def app():
    st.title('Home page')
    st.write("Here will be info and descriptions how to use application")

    html_content = """
    <div style="display: flex; justify-content: center;">
        <a href="https://github.com/piotrulo022/">
            <img src="data:image/jpeg;base64,{}" width="128">
        </a>
    </div>
    """.format(
        b64encode(open("./resources/github.png", "rb").read()).decode()
    )

    st.markdown(html_content, unsafe_allow_html=True)
