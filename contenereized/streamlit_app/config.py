import streamlit as st
import requests
from util_funs import API_URL, SUPPORTED_MODELS
from util_funs import change_model, model_card


# API_URL = os.environ.get('API_URL')
# SUPPORTED_MODELS = ['tarekziade/deit-tiny-distilgpt2', 'Salesforce/blip-image-captioning-base', 'llava-hf/llava-1.5-7b-hf', ]



# def model_card(name):
#     st.title("Model card")

#     # URL to be embedded
#     url = "https://huggingface.co/" + name

#     # Use HTML component to embed a browser window
#     st.components.v1.html(
#         f'<iframe src="{url}" width="100%" height="600" frameborder="0" scrolling="auto"></iframe>',
#         height=800
#     )


# def change_model():
#     with st.spinner(f'Changing model....'):
#         response = requests.post(API_URL + '/change_model/', params = {'name': st.session_state["selected-model"]})

#         if response.status_code == 200:
#             mess = st.success(f"Succesfully switched model to {st.session_state['selected-model']}", icon="✅")
#         else:
#             mess = st.error("Failed to switch model.", icon="🚨") 
#         time.sleep(2)
#         mess.empty()


def app():
    selected_model = st.selectbox(f'Choose model', options = SUPPORTED_MODELS, key = 'selected-model', on_change=change_model)
    
    modelname_response = requests.get(API_URL + '/model_name/')

    model_name = modelname_response.json()['model_name']

    st.markdown(f'Currently used model: ***{model_name}***')

    with st.expander('Model card'):
        model_card(selected_model)

    