import streamlit as st
import requests
import os

API_URL = os.environ.get('API_URL')
SUPPORTED_MODELS = ['tarekziade/deit-tiny-distilgpt2', 'Salesforce/blip-image-captioning-base']



def change_model():
    
    response = requests.post(API_URL + '/change_model/', params = {'name': st.session_state["selected-model"]})
    

def app():
    selected_model = st.selectbox(f'Choose model', options = SUPPORTED_MODELS, key = 'selected-model', on_change=change_model)
    
    
    modelname_response = requests.get(API_URL + '/model_name/')

    model_name = modelname_response.json()['model_name']

    st.markdown(f'Currently used model: ***{model_name}***')

    