import streamlit as st
import requests
from streamlit_option_menu import option_menu
import time
import config, get_caption, homepage, database_preview

import os
import socket

API_URL = os.environ.get('API_URL')


st.set_page_config(
    page_title = "Captioning app"
)

def check_port(host, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        sock.settimeout(1)
        # Attempt to connect to the host and port
        result = sock.connect_ex((host, port))
        # Close the socket
        sock.close()
        # Check if the connection was successful
        if result == 0:
            return f"Port {port} is open on {host}"
        else:
            return f"Port {port} is closed on {host}"
    except socket.error as e:
        return f"Error: {e}"
    

    
def check_fastapi_ready(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

###############TODO: finish
def health_check():
    database_status = check_port('db', 3306)
    st.session_state['database_status'] = database_status # 0- alive, else not alive

    fastapi_status = check_port('model_api', 5000)
    st.session_state['fastapi_stauts'] = database_status # 0- alive, else 

###################

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
            homepage.app()
        if app == "Get caption":
            get_caption.app()
        if app == "Config":
            config.app()
        if app == "Database":
            database_preview.app()

          
    run()            
         