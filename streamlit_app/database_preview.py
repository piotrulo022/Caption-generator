"""
This file is a page of streamlit UI microservice and provides database preview.
"""
import streamlit as st
import pandas as pd

from util_funs import *


def app():
    """
    Database preview page
    """
    
    st.title('Gallery')

    data = get_data()
    df = data['data']

    if len(df) == 0:
        st.write('Nothing here yet. Generate some captions and push them to the database so they will apear here!')

    else:
        df = pd.DataFrame(df, columns=data['colnames'])
        
        
        st.button('Purge database', on_click = delete_all_rows)
        st.markdown("""
                <style>
                .caption-font {
                    font-size:16px !important;
                    font-style: italic;
                }
                </style>
                """, unsafe_allow_html=True)
        

        c1, c2, c3 = st.columns([3, 1, 2], gap = 'medium')

        c1.markdown('## Image')
        c2.markdown('## Model used')
        c3.markdown('## Caption')
        
        for ind, row in df.iterrows(): # draw images stored in database
            image = decode_image(row['image_file']) 
            image.resize((128, 64))

            caption = row['caption']
            created_time = row['created_time']
            model_used = row['model_used']


            del_but, image_col, model_col, caption_col = st.columns([1, 3, 1, 2], gap = 'medium')
            
            image_col.image(image, caption = 'Created at: ' + str(created_time))
            
            model_col.markdown(f'*{model_used}*')

            caption_col.markdown(f'<p class="caption-font"> {caption} </p>', unsafe_allow_html=True)
            
            del_but.button('Delete', on_click = delete_row, key = str(ind), args = (str(created_time), caption))