import streamlit as st
import requests
from util_funs import API_URL, SUPPORTED_MODELS
from util_funs import change_model, model_card


def app():
    selected_model = st.selectbox(f'Choose model', options = SUPPORTED_MODELS, key = 'selected-model', on_change=change_model)
    
    modelname_response = requests.get(API_URL + '/model_name/')

    model_name = modelname_response.json()['model_name']

    st.markdown(f'Currently used model: ***{model_name}***')

    with st.expander('Model card'):
        model_card(selected_model)

    