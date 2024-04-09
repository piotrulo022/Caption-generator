import socket
import requests
import streamlit as st

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

        return result # 0 - OK
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
    

def health_check():
    database_status = check_port('db', 3306)
    fastapi_status = check_port('model_api', 5000)
    
    return {'database_status': database_status,
            'fastapi_status': fastapi_status}




def monitor_health():
    while True:
        statuses = health_check()
        api_status = statuses['fastapi_status']
        database_status = statuses['database_status']

        st.session_state['fastapi_status'] = api_status
        st.session_state['database_status'] = database_status
