import streamlit as st
from streamlit_option_menu import option_menu

import config, get_caption, homepage, database_preview

import time

from util_funs import API_URL
from util_funs import check_backend_status

st.set_page_config(
    page_title = "Captioning app"
)


with st.spinner("Waiting for FastAPI server to start..."): # wait for FastAPI to begin run
    while not check_backend_status(API_URL):
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
                options=['Homepage','Config', 'Generate captions', 'Database'],

                icons=['house-fill', 'gear', 'pen', 'database'],
                menu_icon='chat-text-fill',
                default_index=0)

        if app == "Homepage":
            homepage.app()
        if app == "Generate captions":
            get_caption.app()
        if app == "Config":
            config.app()
        if app == "Database":
            database_preview.app()
    run()            
         