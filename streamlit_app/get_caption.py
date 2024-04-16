"""
This file is a page of streamlit UI microservice and is used to generate captions.
"""

import streamlit as st
import requests
from PIL import Image
from io import BytesIO


from util_funs import API_URL

def app():
    st.title('Caption generator')
    st.write('Pass some images and get captions of them!')

    local, www = st.tabs(['From local', 'From www'])

    # MODE = LOCAL
    with local:
        file = st.file_uploader("Upload a file", type=["jpg", "png", "jpeg", ])
        if file is not None:
            bytes_data = file.getvalue()
            img = Image.open(BytesIO(bytes_data))
            
            st.image(img, caption = file.name, use_column_width=True)
            
            push_db_file = st.checkbox(label = 'Push to the database', value = True, key = 'push_db_file')

            if st.button('Get description', key = 'file_request'):

                files = {'file': (file.name, bytes_data, file.type)}
                response = requests.post(API_URL + '/predict_image_file/',
                                        files = files,
                                        params = {'push_db': push_db_file})
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


    # MODE = WWW

    with www:
        url = st.text_input("Pass www image source", value = "https://raw.githubusercontent.com/piotrulo022/Caption-generator/main/contenereized/backend/tests/elephantoo.png")
        push_db_url = st.checkbox(label = 'Push to the database', value = True, key = 'push_db_url')


        if st.button('Get description', key = 'url_request'):
            with st.spinner('Wait for it...'):
                try:
                    st.image(url)
                except Exception as e:
                    pass
                
                try:
                    response = requests.post(API_URL + '/predict_image_url/',
                                            json = {'url': url,
                                                    'push_db': push_db_url})
                    if response.status_code == 200:
                        response_data = response.json()
                        st.success(f"Image description:\t *{response_data['prediction']}*", icon="✅")
                        st.markdown(f"Processing time: *{response_data['processing_time']}*")
                    else:
                        st.error(f"Failed to get description. Response status code: {response.status_code}", icon="🚨") 
                except Exception as e:
                    st.error(f'An unexpected error occured! {str(e)}')
