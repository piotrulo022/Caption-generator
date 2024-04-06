import streamlit as st
import requests
from streamlit_option_menu import option_menu
import time
import Config, Get_caption, Homepage

st.set_page_config(
    page_title = "Captioning app"
)
def check_fastapi_ready(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

# URL of your FastAPI server
fastapi_url = "http://localhost:8000/"


with st.spinner("Waiting for FastAPI server to start..."):
    while not check_fastapi_ready(fastapi_url):
        time.sleep(1)


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Menu',
                # options=['Home','Account','Trending','Your Posts','about'],
                options=['Homepage','Config', 'Get caption' ],

                icons=['house-fill','gear','trophy-fill'],
                menu_icon='chat-text-fill',
                default_index=0,
                
        #         styles={
        #             "container": {"padding": "5!important","background-color":'black'},
        # "icon": {"color": "white", "font-size": "23px"}, 
        # "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        # "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        
        if app == "Homepage":
            Homepage.app()
        if app == "Get caption":
            Get_caption.app()
        if app == "Config":
            Config.app()

          
    run()            
         