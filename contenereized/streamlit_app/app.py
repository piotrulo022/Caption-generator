import streamlit as st
import requests
from PIL import Image
from io import BytesIO

API_URL = 'http://model_api:5000'
LANG = 'ENGLISH'


# Define Streamlit UI
st.title('Caption generator')

local, www = st.tabs(['From local', 'From www'])


with local:
    file = st.file_uploader("Upload a file", type=["jpg", "png"])
    if file is not None:
        bytes_data = file.getvalue()
        img = Image.open(BytesIO(bytes_data))
        
        st.image(img, caption = file.name, use_column_width=True)
        

        file_prompt = st.text_input(label = 'Additional prompt', value = 'Tell me what it is', key = 'file_prompt')

        if st.button('Get description', key = 'file_request'):

            files = {'file': (file.name, bytes_data, file.type)}
            response = requests.post(API_URL + '/predict_image_file/',
                                     files = files,
                                     params = {'language': LANG,
                                            'prompt': file_prompt})
            
            with st.spinner('Wait for it...'):
                st.write(str(response.json()))
                
                if response.status_code == 200:
                    st.write("*Image description:*")
                    st.markdown(f"***{response.json()['prediction']}***")
                    

                else:
                    st.error("Failed to get description.") 

with www:
    url = st.text_input("Pass www image source", value = "https://www.google.pl/images/branding/googlelogo/1x/googlelogo_light_color_272x92dp.png")
    url_prompt = st.text_input(label = 'Additional prompt', value = 'Tell me what it is', key = 'url_prompt')
    if st.button('Get description', key = 'url_request'):
        with st.spinner('Wait for it...'):
            response = requests.post(API_URL + '/predict_image_url/',
                                     json = {'url': url,
                                             'prompt': url_prompt,
                                             'language': LANG})
            if response.status_code == 200:
                st.write("Response form FastAPI:")
                st.success('Done!')
                st.markdown(f"*{response.json()['prediction']}*")

            else:
                st.error("Failed to get description.")
        