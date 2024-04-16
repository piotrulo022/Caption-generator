import streamlit as st
from base64 import b64encode 

def app():
    st.title('Home page')
    st.markdown(
                """                
                This application serves to generate descriptions for images using AI models provided by [the huggingface transformers library](https://huggingface.co/docs/transformers/). It consists of three functional tabs:
                
                - ***Config*** - tab delivering user an ability to change the model used for caption generating. Currently supported models are [tarekziade/deit-tiny-distilgpt2](https://huggingface.co/tarekziade/deit-tiny-distilgpt2), [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base), [llava-hf/llava-1.5-7b-hf](https://huggingface.co/llava-hf/llava-1.5-7b-hf), [noamrot/FuseCap_Image_Captioning](https://huggingface.co/noamrot/FuseCap_Image_Captioning)
                                
                - ***Generate captions***: Here you can obtain descriptions for images you provide. You can upload a file from their local disk or provide a URL to a webpage containing the image. Also you have the option to save images along with their descriptions in the database.

                - ***Database***: Here you can view saved images and manage them by deleting individual entries or clearing the entire database using the provided buttons. 
                """
                )
    
    
    st.markdown('If you find any issue, please do not hesitate and share it on issues page on project repository.')
    html_content = """
    <div style="display: flex; justify-content: center;">
        <a href="https://github.com/piotrulo022/Caption-generator/">
            <img src="data:image/jpeg;base64,{}" width="128">
        </a>
    </div>
    """.format(
        b64encode(open("./resources/github.png", "rb").read()).decode()
    )

    st.markdown(html_content, unsafe_allow_html=True)
