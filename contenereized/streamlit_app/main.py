import streamlit as st
import requests
from streamlit_option_menu import option_menu
import time
import config, get_caption, Homepage, database_preview

import os

API_URL = os.environ.get('API_URL')



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


with st.spinner("Waiting for FastAPI server to start..."):
    while not check_fastapi_ready(API_URL):
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
            Homepage.app()
        if app == "Get caption":
            get_caption.app()
        if app == "Config":
            config.app()
        if app == "Database":
            database_preview.app()

          
    run()            
         