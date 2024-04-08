import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os


API_URL = os.environ.get('API_URL')

def app():

    # Define Streamlit UI
    st.title('Caption generator')

    local, www = st.tabs(['From local', 'From www'])

    with local:
        file = st.file_uploader("Upload a file", type=["jpg", "png", "jpeg", ])
        if file is not None:
            bytes_data = file.getvalue()
            img = Image.open(BytesIO(bytes_data))
            
            st.image(img, caption = file.name, use_column_width=True)
            
            push_db_file = st.checkbox(label = 'Push to the database', value = True, key = 'push_db_file')


            file_prompt = st.text_input(label = 'Additional prompt', value = 'Tell me what it is', key = 'file_prompt')

            if st.button('Get description', key = 'file_request'):

                files = {'file': (file.name, bytes_data, file.type)}
                response = requests.post(API_URL + '/predict_image_file/',
                                        files = files,
                                        params = {'prompt': file_prompt,
                                                'push_db': push_db_file})
                with st.spinner('Wait for it...'):
                    try:                    
                        if response.status_code == 200:
                            response_data = response.json()
                            st.success(f"Image description:\t *{response_data['prediction']}*", icon="✅")
                            st.markdown(f"Processing time: *{response_data['processing_time']}*")

                        else:
                            st.error("Failed to get description.", icon="🚨") 

                    except Exception as e:
                        st.error(f'An unexpected error occured! {str(e)}')

    with www:
        url = st.text_input("Pass www image source", value = "https://www.google.pl/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png")
        url_prompt = st.text_input(label = 'Additional prompt', value = 'Tell me what it is', key = 'url_prompt')


        push_db_url = st.checkbox(label = 'Push to the database', value = True, key = 'push_db_url')


        if st.button('Get description', key = 'url_request'):
            with st.spinner('Wait for it...'):
                st.image(url)
                try:
                    response = requests.post(API_URL + '/predict_image_url/',
                                            json = {'url': url,
                                                    'prompt': url_prompt,
                                                    'push_db': push_db_url})
                    if response.status_code == 200:
                        response_data = response.json()
                        st.success(f"Image description:\t *{response_data['prediction']}*", icon="✅")
                        st.markdown(f"Processing time: *{response_data['processing_time']}*")
                    else:
                        st.error(f"Failed to get description. Response status code: {response.status_code}", icon="🚨") 
                except Exception as e:
                    st.error(f'An unexpected error occured! {str(e)}')
