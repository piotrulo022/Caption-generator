import streamlit as st
from streamlit_option_menu import option_menu

import config, get_caption, homepage, database_preview

import time
import requests
import os

API_URL = os.environ.get('API_URL') # get OS environment variable for API URL adress


# Define page setting is config
st.set_page_config(
    page_title = "Captioning app"
)



def check_service_status(url):
    """
    This funcion checks wheter URL is available and is used to monitor FastAPI container status.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False
    


with st.spinner("Waiting for FastAPI server to start..."): # wait for FastAPI to begin run
    while not check_service_status(API_URL):
        time.sleep(4)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        with st.sidebar:        
            app = option_menu(
                menu_title='Menu',
                options=['Homepage','Config', 'Get caption', 'Database'],

                icons=['house-fill', 'gear', 'pen', 'database'],
                menu_icon='chat-text-fill',
                default_index=0)

        if app == "Homepage":
            homepage.app()
        if app == "Get caption":
            get_caption.app()
        if app == "Config":
            config.app()
        if app == "Database":
            database_preview.app()
    run()            
         