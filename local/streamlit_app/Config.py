import streamlit as st
import requests

SUPPORTED_MODELS = ['tarekziade/deit-tiny-distilgpt2', 'Salesforce/blip-image-captioning-base']

def change_model():
    
    response = requests.post('http://localhost:8000/change_model/', params = {'name': st.session_state["selected-model"]})
    
def get_selected_model():
    global SELECTED_MODEL

    modelname_response = requests.get('http://localhost:8000/model_name/')

    model_name = modelname_response.json()['model_name']



def app():
    selected_model = st.selectbox(f'Choose model', options = SUPPORTED_MODELS, key = 'selected-model', on_change=change_model)
    
    # change_model(selected_model)

    modelname_response = requests.get('http://localhost:8000/model_name/')

    model_name = modelname_response.json()['model_name']
    st.markdown(f'Currently used model: ***{model_name}***')

    