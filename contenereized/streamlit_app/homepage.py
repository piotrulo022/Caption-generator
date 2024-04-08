import streamlit as st
from base64 import b64encode 

def app():
    st.title('Home page')
    st.write("Here will be info and descriptions how to use application")


    st.markdown(
    """<a href="https://github.com/piotrulo022/">
    <img src="data:image/jpeg;base64,{}" width="25">
    </a>""".format(
        b64encode(open("./resources/github.jpeg", "rb").read()).decode()
    ),
    unsafe_allow_html=True,

)
